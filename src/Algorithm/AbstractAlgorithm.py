from abc import ABCMeta, abstractmethod


class AbstractAlgorithm(object, metaclass=ABCMeta):

    def __init__(self, problem):
        self.problem = problem

    def __str__(self):
        s = "|-=-=-=-=-=-=-=-=-= [ Algorithm ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|\n"
        s += "| Name : " + self.__class__.__name__ + "\n"
        s += str(self.problem)
        return s

    @abstractmethod
    def compute(self):
        raise NotImplementedError
