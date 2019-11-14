from defaults.defaults_data import get_default, update_site_default
from hybrid.scenario import run_default_scenario
from hybrid.storage import storage
from hybrid.systems_behavior import get_system_behavior_fx
from parameters.parameter_data import get_input_output_data
import matplotlib.pyplot as plt
import seaborn as sns

# Check https://nrel-pysam.readthedocs.io/en/latest/modules/StandAloneBattery.html for details
# This is the default PV plus single owner case, with a battery enabled, and using
# A fixed PPA price of $.10/kWh, and using the default hourly TOD factors.
def test_storage():
    plot_dispatch = False
    technologies = ['Solar', 'Generic', 'Battery']
    systems = get_system_behavior_fx(technologies)  # defines which models get run in each system
    defaults, site = get_default(technologies)
    site['lat'] = 33.450495
    site['lon'] = -111.983688
    site['elev'] = 358
    site['tz'] = -7
    site['year'] = '2012'
    defaults = update_site_default(defaults, site)
    defaults['Battery']['StandAloneBattery']['Battery']['en_batt'] = 1

    # Modify battery size


    # Automated front of meter with energy market price signal
    defaults['Battery']['StandAloneBattery']['Battery']['batt_meter_position'] = 1
    defaults['Battery']['StandAloneBattery']['Battery']['batt_dispatch_choice'] = 0
    defaults['Battery']['StandAloneBattery']['Battery']['batt_dispatch_auto_can_charge'] = 1
    defaults['Battery']['StandAloneBattery']['Battery']['batt_dispatch_auto_can_gridcharge'] = 0
    defaults['Battery']['StandAloneBattery']['Battery']['batt_cycle_cost_choice'] = 1
    defaults['Battery']['StandAloneBattery']['Battery']['batt_cycle_cost'] = 0.005

    # multiplier on the PPA price, that applies to selling energy during the hour, e.g, 0.7 for $.05/kWh = $0.035 /kWh
    tod_factors = [0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1.2,1.2,1.2,1.2,2.064,2.064,2.064,2.064,2.064,2.064,1.2,1.2,1.2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.8,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0.8,0.8,0.8]
    for tech in defaults:
        defaults[tech]['Singleowner']['SolutionMode']['ppa_soln_mode'] = 1 # input PPA price
        defaults[tech]['Singleowner']['PPAPrice']['ppa_price_input'] = 0.1 # $/kWh
        defaults[tech]['Singleowner']['TimeOfDelivery']['ppa_multiplier_model'] = 1 # use the TOD factors
        defaults[tech]['Singleowner']['TimeOfDelivery']['dispatch_factors_ts'] = tuple(tod_factors)

    input_data, output_data = get_input_output_data(systems)

    scenario, outputs = run_default_scenario(defaults=defaults,
                                             input_info=input_data,
                                             output_info=output_data,
                                             run_systems=systems)


    assert round(outputs['Battery']['average_battery_roundtrip_efficiency']) == 80
    assert len(outputs['Battery']['gen']) == 8760

    batt_power = outputs['Battery']['batt_power']
    sell_rate = outputs['Battery']['market_sell_rate_series_yr1']


    if plot_dispatch:
        day_start = 157
        day_end = 159

        dict_plot = dict()
        dict_plot['Time (hour of year)'] = range(day_start * 24, day_end * 24)
        dict_plot['Battery power (kW)'] = batt_power[day_start*24:day_end*24]
        dict_plot['Market rate ($/MWh)'] = sell_rate[day_start*24:day_end*24]



        #sns.set(style="darkgrid")
        fig, ax1 = plt.subplots()

        ax1.plot(dict_plot['Time (hour of year)'], dict_plot['Battery power (kW)'], color='b', label='Battery power')
        ax2 = ax1.twinx()
        ax2.plot(dict_plot['Time (hour of year)'], dict_plot['Market rate ($/MWh)'], color='g', label='Market rate')
        ax1.set_xlabel('Hour of year')
        ax1.set_ylabel('Battery Power (kW)')
        ax2.set_ylabel('Sell Rate ($/MWh)')
        h0, l0 = ax1.get_legend_handles_labels()
        h1, l1 = ax2.get_legend_handles_labels()
        plt.legend(h0 + h1, l0 + l1, loc=2)
        plt.show()


def test_storage_sizing():

    batt_kw_desired = 30000 # 30 MW
    batt_kwh_desired = 120000 # 120 MWh

    technologies = ['Solar', 'Generic', 'Battery']
    systems = get_system_behavior_fx(technologies)  # defines which models get run in each system
    defaults, site = get_default(technologies)
    site['lat'] = 33.450495
    site['lon'] = -111.983688
    site['elev'] = 358
    site['tz'] = -7
    site['year'] = '2012'
    defaults = update_site_default(defaults, site)
    defaults['Battery']['StandAloneBattery']['Battery']['en_batt'] = 1

    # size the battery
    defaults = storage.size_storage(defaults, batt_kw_desired, batt_kwh_desired)

    assert round(defaults['Battery']['StandAloneBattery']['Battery']['batt_computed_strings']) == 106581
    assert round(defaults['Battery']['StandAloneBattery']['Battery']['batt_computed_series']) == 139
    assert round(defaults['Battery']['StandAloneBattery']['Battery']['batt_computed_bank_capacity']) == 120000







