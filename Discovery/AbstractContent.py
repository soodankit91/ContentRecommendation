import abc

class AbstractContentSource(abc.ABC):
    @abc.abstractmethod
    def adaptToES(ids, links, titles, descriptions, tags):
        pass
