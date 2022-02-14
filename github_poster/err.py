class BaseDrawError(Exception):
    """
    draw github poster wrong
    """

    pass


class CircularDrawError(BaseDrawError):
    """
    draw circular poster wrong
    """

    pass


class DepNotInstalledError(Exception):
    def __str__(self):
        return self.args[0]
