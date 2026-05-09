class ClassifierFactory:

    @classmethod
    def get(cls, name: str, **kwargs):
        pass

    @classmethod
    def available(cls) -> list[str]:
        pass


class RegressorFactory:

    @classmethod
    def get(cls, name: str, **kwargs):
        pass

    @classmethod
    def available(cls) -> list[str]:
        pass
