# Convert Cassandra UUID Field to Pydantic Datetime Str 
import datetime

def uuid1_time_to_datetime(time: int):
    """
    Converts a time value from a UUID1 field in Cassandra to a Python datetime object.
    The start datetime is set to October 15th, 1582.
    The time value is added to the start datetime, divided by 10 (ignoring the remainder).
    """
    return datetime.datetime(1582, 10, 15) + datetime.timedelta(microseconds=time // 10)
