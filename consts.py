from enum import Enum

class GroupTypes(Enum):
    WHITE = "White list based group"
    BLACK = "Black list based group"

class UserTypes(Enum):
    IN_BLACKLIST = "0"
    COMMON = "1"
    IN_WHITELIST = "2"
    MODERATOR = "3"

class DataBaseResponses(Enum):
    SUCCESS = "operation successful"
    ERROR = "operation unsuccessful"