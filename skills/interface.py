from abc import ABC, abstractmethod


class BaseSkill(ABC):

    @abstractmethod
    def run(self, params: str) -> dict:
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

    @abstractmethod
    def _create_answer_packet(self, status_code, data=None):
        """

        @param status_code: int
        @param data: Optional[str]
        @return: str
        """
