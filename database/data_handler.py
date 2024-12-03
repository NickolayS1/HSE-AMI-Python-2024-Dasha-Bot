from consts import DataBaseResponses
from consts import GroupTypes
from consts import UserTypes


class DataBase:
    def __init__(self):
        pass

    def get_type_of_group(self, group_id: int) -> DataBaseResponses:
        pass

    def set_type_of_group(self, group_id: int, group_type: GroupTypes) -> DataBaseResponses:
        pass

    def get_user_type(self, user_id: int, group_id: int) -> UserTypes:
        pass

    def set_user_type(self, user_id: int, group_id: int, new_type: UserTypes) -> DataBaseResponses:
        pass

    def get_user_id_list(self, group_id: int) -> list[int]:
        pass
    
    def get_amount_of_maximum_warns(self, group_id: int) -> int:
        pass

    def set_amount_of_maximum_warns(self, group_id: int) -> int:
        pass

    def get_amounts_of_warns(self, user_id: int, group_id: int) -> int:
        pass

    def get_groups_list(self, user_id: int) -> list[int]:
        pass