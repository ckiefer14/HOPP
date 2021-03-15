import sys, os

import pyomo.environ as pyomo
from pyomo.opt import TerminationCondition
from pyomo.util.check_units import assert_units_consistent

from hybrid.sites import SiteInfo
from hybrid.dispatch.solar_dispatch import SolarDispatch
from hybrid.dispatch.wind_dispatch import WindDispatch
from hybrid.dispatch.battery_dispatch import BatteryDispatch
from hybrid.dispatch.grid_dispatch import GridDispatch


class HybridDispatchOptions:
    """

    """
    def __init__(self, dispatch_options: dict = None):
        self.include_battery_lifecycle_cost: bool = False
        self.use_simple_battery_dispatch: bool = True
        self.n_look_ahead_periods: int = 48
        self.n_roll_periods: int = 24
        self.log_name: str = 'hybrid_dispatch_optimization.log'

        if dispatch_options is not None:
            for key, value in dispatch_options.items():
                if hasattr(self, key):
                    if type(getattr(self, key)) == type(value):
                        setattr(self, key, value)
                    else:
                        raise ValueError("'{}' is the wrong data type.".format(key))
                else:
                    raise NameError("'{}' is not an attribute in {}".format(key, type(self).__name__))


class HybridDispatch:
    """

    """
    def __init__(self,
                 site: SiteInfo,
                 power_sources: dict,
                 dispatch_options: dict = None):

        self.site: SiteInfo = site
        self.power_sources = power_sources

        self.options = HybridDispatchOptions(dispatch_options)

        if os.path.isfile(self.options.log_name):
            os.remove(self.options.log_name)

        self.needs_dispatch = 'battery' in self.power_sources.keys()

        if self.needs_dispatch:
            self._pyomo_model = self.create_dispatch_optimization_model()
            self.create_gross_profit_objective()
            self.initialize_dispatch_model_parameters()
            self.create_arcs()
            assert_units_consistent(self.pyomo_model)

    def create_dispatch_optimization_model(self):
        """
        Creates monolith dispatch model
        """
        model = pyomo.ConcreteModel(name='hybrid')
        #################################
        # Sets                          #
        #################################
        model.forecast_horizon = pyomo.Set(doc="Set of time periods in time horizon",
                                           initialize=range(self.options.n_look_ahead_periods))
        #################################
        # Blocks (technologies)         #
        #################################
        for source, tech in self.power_sources.items():
            if source is 'solar':
                tech._dispatch = SolarDispatch(model, model.forecast_horizon)
            elif source is 'wind':
                tech._dispatch = WindDispatch(model, model.forecast_horizon)
            elif source is 'battery':
                tech._dispatch = BatteryDispatch(model, model.forecast_horizon,
                                                 include_lifecycle_cost=self.options.include_battery_lifecycle_cost,
                                                 use_simple_battery_dispatch=self.options.use_simple_battery_dispatch)
            elif source is 'grid':
                tech._dispatch = GridDispatch(model, model.forecast_horizon, self.power_sources)
            else:
                ValueError("'{}' is not supported in the hybrid dispatch model.".format(source))
        return model

    def gross_profit_objective_rule(self, m):
        objective = 0.0
        for tech in self.power_sources.values():
            objective += tech.dispatch.gross_profit_objective_rule(m)
        return objective

    def create_gross_profit_objective(self):
        self.pyomo_model.gross_profit_objective = pyomo.Objective(rule=self.gross_profit_objective_rule, sense=pyomo.maximize)

    def create_arcs(self):
        if 'grid' in self.power_sources.keys():
            self.power_sources['grid'].dispatch.create_arcs()

        pyomo.TransformationFactory("network.expand_arcs").apply_to(self.pyomo_model)

    def initialize_dispatch_model_parameters(self):
        for tech in self.power_sources.values():
            tech.initialize_dispatch_model_parameters()

    def update_time_series_dispatch_model_parameters(self, start_time: int):
        for tech in self.power_sources.values():
            tech.update_time_series_dispatch_model_parameters(start_time)

    def update_electricity_prices(self, prices: list):
        for tech in self.power_sources.values():
            if tech is not 'grid':
                tech.dispatch.electricity_sell_price = prices

    @staticmethod
    def glpk_solve_call(pyomo_model: pyomo.ConcreteModel,
                        log_name: str = None):
        solver = pyomo.SolverFactory('glpk')  # Ref. on solver options: https://en.wikibooks.org/wiki/GLPK/Using_GLPSOL
        solver_options = {'cuts': None,
                          #'mipgap': 0.001,
                          #'tmlim': 30
                          }

        if log_name is not None:
            solver_options['log'] = 'dispatch_instance.log'

        # This is to remove a super annoying warning -> by adding a null var and constraint
        # "WARNING  Empty constraint block written in LP format - solver may error"
        # This comes from nested blocks... pyomo\repn\plugins\cpxlp.py line 711
        # pyomo_model.one_var = pyomo.Var()
        # pyomo_model.one_constraint = pyomo.Constraint(expr=pyomo_model.one_var == 1.0)

        results = solver.solve(pyomo_model, options=solver_options)

        if log_name is not None:
            HybridDispatch.append_solve_to_log(log_name, solver_options['log'])

        if results.solver.termination_condition == TerminationCondition.infeasible:
            HybridDispatch.print_infeasible_problem(pyomo_model)
        return results

    def glpk_solve(self):
        return HybridDispatch.glpk_solve_call(self.pyomo_model, self.options.log_name)

    @staticmethod
    def mindtpy_solve_call(pyomo_model: pyomo.ConcreteModel,
                           log_name: str = None):
        solver = pyomo.SolverFactory('mindtpy')

        if log_name is not None:
            solver_options = {'log': 'dispatch_instance.log'}

        results = solver.solve(pyomo_model,
                               mip_solver='glpk',
                               nlp_solver='ipopt',
                               tee=True)

        if log_name is not None:
            HybridDispatch.append_solve_to_log(log_name, solver_options['log'])

        if results.solver.termination_condition == TerminationCondition.infeasible:
            HybridDispatch.print_infeasible_problem(pyomo_model)
        return results

    @staticmethod
    def append_solve_to_log(log_name: str, solve_log: str):
        # Appends single problem instance log to annual log file
        fin = open(solve_log, 'r')
        data = fin.read()
        fin.close()

        ann_log = open(log_name, 'a+')
        ann_log.write("=" * 50 + "\n")
        ann_log.write(data)
        ann_log.close()

    @staticmethod
    def print_infeasible_problem(model: pyomo.ConcreteModel):
        original_stdout = sys.stdout
        with open('infeasible_instance.txt', 'w') as f:
            sys.stdout = f
            print('\n' + '#' * 20 + ' Model Parameter Values ' + '#' * 20 + '\n')
            HybridDispatch.print_all_parameters(model)
            print('\n' + '#' * 20 + ' Model Blocks Display ' + '#' * 20 + '\n')
            HybridDispatch.display_all_blocks(model)
            sys.stdout = original_stdout
        raise ValueError("Dispatch optimization model is infeasible.\n"
                         "See 'infeasible_instance.txt' for parameter values.")

    @staticmethod
    def print_all_parameters(model: pyomo.ConcreteModel):
        param_list = list()
        block_list = list()
        for param_object in model.component_objects(pyomo.Param, active=True):
            name_to_print = param_object.getname()
            parent_block = param_object.parent_block().parent_component()
            block_name = parent_block.getname()
            if (name_to_print not in param_list) or (block_name not in block_list):
                block_list.append(block_name)
                param_list.append(name_to_print)
                print("\nParent Block Name: ", block_name)
                print("Parameter: ", name_to_print)
                for index in parent_block.index_set():
                    val_to_print = pyomo.value(getattr(parent_block[index], param_object.getname()))
                    print("\t", index, "\t", val_to_print)

    @staticmethod
    def display_all_blocks(model: pyomo.ConcreteModel):
        for block_object in model.component_objects(pyomo.Block, active=True):
            for index in block_object.index_set():
                block_object[index].display()

    def simulate(self, is_test: bool = False):
        # Dispatch Optimization Simulation with Rolling Horizon
        # Solving the year in series
        ti = list(range(0, self.site.n_timesteps, self.options.n_roll_periods))
        for i, t in enumerate(ti):
            print('Evaluating day ', i, ' out of ', len(ti))
            self.simulate_with_dispatch(t)
            # TODO: Remove for release
            if is_test and i > 10:
                break

    def simulate_with_dispatch(self,
                               start_time: int,
                               n_days: int = 1,
                               initial_soc: float = None,
                               n_initial_sims: int = 0):
        # this is needed for clustering effort
        update_dispatch_times = list(range(start_time,
                                           start_time + n_days * self.site.n_periods_per_day,
                                           self.options.n_roll_periods))

        for i, sim_start_time in enumerate(update_dispatch_times):
            # Update battery initial state of charge
            if 'battery' in self.power_sources.keys():
                self.power_sources['battery'].update_dispatch_initial_soc(initial_soc=initial_soc)
                initial_soc = None

            for model in self.power_sources.values():
                model.update_time_series_dispatch_model_parameters(sim_start_time)
            self.glpk_solve()

            if i < n_initial_sims:
                sim_start_time = None

            # step through dispatch solution for battery and simulate battery
            if 'battery' in self.power_sources.keys():
                self.power_sources['battery'].simulate_with_dispatch(self.options.n_roll_periods,
                                                                     sim_start_time=sim_start_time)

    @property
    def pyomo_model(self) -> pyomo.ConcreteModel:
        return self._pyomo_model

    @property
    def gross_profit_objective(self):
        return pyomo.value(self.pyomo_model.gross_profit_objective)
