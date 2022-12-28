from abc import ABC, abstractmethod


class BaseSkill(ABC):

    @abstractmethod
    def run(self, params: str) -> None:
        """

        @param params: dict
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
