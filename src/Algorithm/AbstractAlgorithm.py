from abc import ABCMeta, abstractmethod
from copy import deepcopy
from src.Utility import AutoNumber
from src.Problem import BordaProperty


class AbstractAlgorithm(object, metaclass=ABCMeta):

    class Status(AutoNumber):
        INITIALIZED = ()
        SUCCEEDED = ()
        FAILED = ()

    def __init__(self, problem):
        self.problem = deepcopy(problem)
        self.sequence = list()
        self.status = self.Status.INITIALIZED
        self.reason = ""
        self.trace = list()

    def __str__(self):
        s = "|-=-=-=-=-=-=-=-=-= [ Status ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|\n"
        s += "| Algorithm\t: " + self.__class__.__name__ + "\n"
        s += "| Sequence\t: " + str(self.sequence) + "\n"
        s += "| Status\t: " + self.status.name + "\n"
        if self.status == self.Status.FAILED:
            s += "| Reason\t: " + self.reason + "\n"
        s += "|\n"
        s += str(self.problem)
        if self.status == self.Status.SUCCEEDED:
            s += self.get_properties_output()
        return s

    def compute(self, sequence, display_trace=True):
        self.trace.clear()
        self.sequence = sequence

        self.trace.append(str(self))
        self.trace.append(self.print_start_computing())

        self._compute(sequence)

        self.problem.compute_borda_properties()

        self.trace.append(self.print_end_computing())
        self.trace.append(str(self))

        if display_trace:
            for trace in self.trace:
                print(trace)

    @abstractmethod
    def _compute(self, sequence):
        raise NotImplementedError

    def get_properties_output(self):
        s = "|-=-=-=-=-=-=-=-=-= [ PROPERTIES ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|\n"
        s += "| Is borda optimal           : " + str(self.problem.borda_properties[BordaProperty.BP]) + "\n"
        s += "| Is borda proportional      : " + str(self.problem.borda_properties[BordaProperty.BE]) + "\n"
        s += "| Is borda max min           : " + str(self.problem.borda_properties[BordaProperty.BM]) + "\n"
        s += "| Is borda maximum borda sum : " + str(self.problem.borda_properties[BordaProperty.BS]) + "\n"
        s += "|\n"
        s += "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        return s

    @staticmethod
    def print_start_computing():
        s = "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        s += "|-=-=-=-=-=-=-=-=-= [ START ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        return s

    @staticmethod
    def print_progress():
        s = "| Sequence"
        return s

    @staticmethod
    def print_end_computing():
        s = "\n|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        s += "|-=-=-=-=-=-=-=-=-= [ END ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        return s
