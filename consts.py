from enum import Enum

class GroupTypes(Enum):
    WHITE = "White list based group"
    BLACK = "Black list based group"

class UserTypes(Enum):
    IN_BLACKLIST = "User is in the black list of this group"
    IN_WHITELIST = "User is in the white list of this grop"
    MODERATOR = "User is moderator"

class DataBaseResponses(Enum):
    SUCCESS = "operation successful"
    ERROR = "operation insuccessful"
    IS_BAN = "user goes to ban"