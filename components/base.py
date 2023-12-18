from dataclasses import dataclass as component


@component
class BaseComponent:
    def __str__(self) -> str:
        return (self.__class__.__name__).lower()
