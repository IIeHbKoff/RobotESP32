from abc import ABC, abstractmethod


class BaseSkill(ABC):

    @abstractmethod
    def __init__(self, bus=None) -> None:
        """

        @param bus: connect
        """

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