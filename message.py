from datetime import datetime
from dataclasses import dataclass


@dataclass
class Message:
    msg_datetime: datetime
    msg_speaker: str
    msg_body: str

    def get_metadata(self):
        return f"{self.get_date()} , {self.get_time().hour}:{self.get_time().min} -- {self.msg_speaker}"

    def get_date(self) -> datetime.date:
        return self.msg_datetime.date()

    def get_time(self) -> datetime.time:
        return self.msg_datetime.time()

    def get_hourmin(self):
        """return 2-tup (hh:mm)"""
        t = self.msg_datetime.time()
        return t.hour, t.min

    # add notes to message
