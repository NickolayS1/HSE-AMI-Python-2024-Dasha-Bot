from consts import DataBaseResponses
from consts import GroupTypes
from consts import UserTypes


class DataBase:
    def __init__(self):
        pass

    def get_type_of_group(self) -> DataBaseResponses:
        pass

    def set_type_of_group(self, group_type: GroupTypes) -> DataBaseResponses:
        pass

    def get_user_state(self, user_id: int) -> UserTypes:
        pass

    def set_user_state(self, user_id: int, new_type: UserTypes) -> DataBaseResponses:
        pass

    def get_user_id_list(self) -> list[int]:
        pass
    
    def get_amount_of_maximum_warns(group_id: int) -> int:
        pass

    def set_amount_of_maximum_warns(group_id: int) -> int:
        pass

    def get_amounts_of_warns(self, group_id: int) -> int:
        pass

    def get_groups_list(self, user_id: int) -> list[int]:
        pass