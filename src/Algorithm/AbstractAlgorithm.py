from abc import ABCMeta, abstractmethod
from copy import deepcopy


class AbstractAlgorithm(object, metaclass=ABCMeta):

    def __init__(self, problem):
        self.problem = deepcopy(problem)
        self.sequence = list()

    def __str__(self):
        s = "|-=-=-=-=-=-=-=-=-= [ Status ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|\n"
        s += "| Algorithm : " + self.__class__.__name__ + "\n"
        s += "| Sequence : " + str(self.sequence) + "\n"
        s += "|\n"
        s += str(self.problem)
        return s

    def compute(self, sequence):
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
