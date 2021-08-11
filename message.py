from datetime import datetime
from dataclasses import dataclass

import db


@dataclass
class Message:
    msg_id: int
    msg_fileref: int
    msg_datetime: datetime
    msg_speaker: str
    msg_body: str
    msg_notes: str


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

    def add_note(self, conn, note: str):
        db.add_note(conn, self.msg_id, note)
