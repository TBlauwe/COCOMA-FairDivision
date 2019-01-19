from abc import ABCMeta, abstractmethod
from copy import deepcopy
from src.Utility import AutoNumber


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
        return s

    def compute(self, sequence):
        self.sequence = sequence

        print(self)
        self.print_start_computing()

        self._compute(sequence)

        self.print_end_computing()
        print(self)

    @abstractmethod
    def _compute(self, sequence):
        raise NotImplementedError

    @staticmethod
    def print_start_computing():
        s = "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        s += "|-=-=-=-=-=-=-=-=-= [ START ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        print(s)

    @staticmethod
    def print_progress():
        s = "| Sequence"
        print(s)

    @staticmethod
    def print_end_computing():
        s = "\n|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        s += "|-=-=-=-=-=-=-=-=-= [ END ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        print(s)
