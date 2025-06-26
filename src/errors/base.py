class ModelTypeError(ValueError):
    pass


class NoItemsMatchedError(Exception):
    pass


class DatabaseNotInitializedError(Exception):
    def __init__(self, message: str = "Database not initialized in state. Ensure to set it before accessing."):
        super().__init__(message)