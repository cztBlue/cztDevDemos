class Event:
    def __init__(
        self, event_name, data=None, message="", cause="", sender=None, receiver=None
    ):
        self.event_name = event_name
        self.message = message
        self.cause = cause
        self.data = data
        self.sender = sender
        self.receiver = receiver

    """
    sender → Mounter → receiver(do eventhandler)
    """