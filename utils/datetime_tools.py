from dateutil import tz

from datetime import datetime, timedelta



def get_difference_time(date: datetime):
    _tz = tz.gettz("Europe/Moscow")
    date = date.replace(tzinfo=_tz)
    return abs(int(date.timestamp() - datetime.now(tz=_tz).timestamp()))


class DateTime:
    def __init__(self):
        self.time_zone = tz.gettz("Europe/Moscow")

    def now(self):
        return datetime.now(tz=self.time_zone)

    def timestamp(self) -> int:
        return int(self.now().timestamp())

    def time_strftime(self, strftime: str = "%d.%m.%Y %H:%M"):
        return self.now().strftime(strftime)

    def format_datetime(self, date: datetime, strftime: str = "%d.%m.%Y %H:%M"):
        return date.strftime(strftime)

    def get_delta_time(self, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
        return self.now() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    def get_normalize_delta_time(self, days: int = 0):
        # 05.30 00:00 (-1) ->

        if self.now().hour != 0 and self.now().minute != 0:
            days += 1

        return self.now().replace(hour=0, minute=0) + timedelta(days=days)

    def convert_timestamp(self, _timestamp: int, strftime: str = "%d.%m.%Y %H:%M") -> dict:
        dt_object = datetime.fromtimestamp(_timestamp, tz=self.time_zone)
        return {
            "dt": dt_object,
            "str": dt_object.strftime(strftime)
        }





