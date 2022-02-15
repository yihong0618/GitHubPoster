class BaseDrawError(Exception):
    """
    draw github poster wrong
    """


class CircularDrawError(BaseDrawError):
    """
    draw circular poster wrong
    """


class DepNotInstalledError(Exception):
    """
    optional dependency not installed
    """
