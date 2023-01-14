try:
    from abc import ABC, abstractmethod
except ImportError:
    from libs.abc import ABC, abstractmethod


class BaseSkill(ABC):

    @abstractmethod
    def run(self) -> None:
        """
        @return: dict
        """

    @abstractmethod
    @property
    def skill_tag(self) -> str:
        """
        @return: str
        """

    @abstractmethod
    @property
    def class_name(self) -> str:
        """
        @return: str
        """
