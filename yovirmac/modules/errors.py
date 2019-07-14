class BaseError(Exception):
    pass


class LowerCommandError(BaseError):
    pass


class UndefinedArgument(BaseError):
    pass


class UndefinedBehaviour(BaseError):
    pass
