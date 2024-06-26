class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Results(metaclass=SingletonMeta):

    def __init__(self):
        self.results = []

    # Returns the iteration, the temperature and the score
    def addResult(self, result: tuple[int, int, float, int]):
        self.results.append(result)

    def getResults(self) -> list[tuple[int, int, float, int]]:
        return self.results