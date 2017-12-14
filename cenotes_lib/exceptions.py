class CenotesError(Exception):
    base_text = "Cenotes Error"


class InvalidUsage(CenotesError):
    base_text = "Invalid usage"

    def __init__(self, *args, **kwargs):
        self.base_text = ",".join(args or kwargs.values())
