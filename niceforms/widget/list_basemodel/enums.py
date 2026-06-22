from enum import StrEnum


class ActionType(StrEnum):
    READ = 'read'
    EDIT = 'edit'
    CREATE = 'create'