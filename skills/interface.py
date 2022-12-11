from abc import ABC, abstractmethod


class BaseSkill(ABC):

    @abstractmethod
    def run(self, params: dict) -> dict:
        """

        @param params: dict
        @return: dict
        """

    @abstractmethod
    @property
    def skill_tag(self):
        """
        @return: str
        """

    @abstractmethod
    @property
    def class_name(self):
        """
        @return: str
        """