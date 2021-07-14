from datetime import datetime

class Message:
    def __init__(self, dt, sender, msg):
        self.__datetime = dt
        self.__sender = sender
        self.__msg = msg

    def get_metadata(self):
        return f"{self.get_date()} , {self.get_time().hour}:{self.get_time().min} -- {self.__sender}"

    def get_date(self) -> datetime.date:
        return self.__datetime.date()

    def get_time(self) -> datetime.time:
        return self.__datetime.time()

    def get_hourmin(self):
        """return 2-tup (hh:mm)"""
        t = self.__datetime.time()
        return (t.hour, t.min)

    def get_message(self):
        return self.__msg

    def __str__(self):
        return self.get_metadata() + ": " + self.get_message()

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.get_metadata() == other.get_metadata() and self.get_message() == other.get_message()
        else:
            return False

    ## timeDifference(self, other):  #returns difference in time between two messages in mins