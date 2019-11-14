from abc import abstractmethod
from typing import (
    Optional,
    Tuple,
    )


class AskTellOptimizer:
    """
    An Ask-Tell structured optimizer, following the recommendations from
    Collette, Y., N. Hansen, G. Pujol, D. Salazar Aponte and R. Le Riche (2010).
    On Object-Oriented Programming of Optimizers - Examples in Scilab.
    In P. Breitkopf and R. F. Coelho, eds.: Multidisciplinary Design Optimization in Computational Mechanics, Wiley,
    pp. 527-565;
    http://www.cmap.polytechnique.fr/~nikolaus.hansen/collette2010Chap14.pdf

    Example usage:
    while not opt.stop():
        x = opt.ask()
        y = f(x)
        opt.tell(x, y)
    return opt.best()
    """
    
    @abstractmethod
    def setup(self, dimension: [any]) -> None:
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """
        :return: True when the optimizer thinks it has reached a stopping point
        """
        pass
    
    @abstractmethod
    def ask(self, num: Optional[int] = None) -> [any]:
        """
        :param num: the number of search points to return. If undefined, the optimizer will choose how many to return.
        :return: a list of search points generated by the optimizer
        """
        pass
    
    @abstractmethod
    def tell(self, evaluations: [Tuple[float, any]]) -> None:
        """
        Updates the optimizer with the objective evaluations of a list of search points
        :param evaluations: a list of tuples of (evaluation, search point)
        """
        pass
    
    @abstractmethod
    def best(self) -> any:
        """
        :return: the current best solution
        """
        pass
    
    def get_num_candidates(self) -> Optional[int]:
        """
        :return: Suggested number of candidates to ask for (for parallel asking), or None for no suggestion
        """
        return None
