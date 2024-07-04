"""My exceptions."""


class ChannelNumberError(Exception):
    """Exception raised for an incorrect number of channels."""

    def __init__(self, msg: str) -> None:
        """
        Set error message.

        E.g.,:
            msg = 'two'
            msg = 'larger than two'
        """
        self.msg = f"The number of channles must be {msg}."
        super().__init__(self.msg)
        self.__class__.__module__ = "__main__"
