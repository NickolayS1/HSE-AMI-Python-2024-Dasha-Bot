from consts import DataBaseResponses
from consts import GroupTypes
from consts import UserTypes


class DataBase:
    def __init__(self):
        pass

    def get_type_of_group(self, group_id: int) -> DataBaseResponses:
        """
        Gets the type of the group via group_id
        """
        pass

    def set_type_of_group(self, group_id: int, group_type: GroupTypes) -> DataBaseResponses:
        """
        Sets new type of the group via group_id
        """
        pass

    def get_user_type(self, user_id: int, group_id: int) -> UserTypes:
        """
        Gets user type in a specified group via user_id and group_id
        """
        pass

    def set_user_type(self, user_id: int, group_id: int, new_type: UserTypes) -> DataBaseResponses:
        """
        Sets new user type in a specified group via user_id and group_id
        """
        pass

    def get_user_id_list(self, group_id: int) -> list[int]:
        """
        Gets user_id list from the specified group via group_id
        """
        pass
    
    def get_amount_of_maximum_warns(self, group_id: int) -> int:
        """
        Gets the maximum number of warns before users get banned
        """
        pass

    def set_amount_of_maximum_warns(self, group_id: int) -> int:
        """
        Sets the maximum number of warns before users get banned
        """
        pass

    def get_amounts_of_warns(self, user_id: int, group_id: int) -> int:
        """
        Gets the number of warns of the specified user via user_id and group_id
        """
        pass

    def get_groups_list(self, user_id: int) -> list[int]:
        """
        Gets the list of [group_id] for each group that uses this Telegram bot
        """
        pass