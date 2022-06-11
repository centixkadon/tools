
from datetime import datetime
import time

def main():
  time_format = "%Y-%m-%d %H:%M:%S"
  # time_str = "1000-01-01 00:00:00"
  time_str = "2000-12-31 23:59:59"
  # time_format = "%Y-%m-%d"
  # time_str = "1000-01-01"

  time_struct = time.strptime(time_str, time_format)
  print(f"str({time_str}) -> time.strptime -> struct({time_struct})")

  time_str = time.strftime(time_format, time_struct)
  print(f"str({time_str}) <- time.strftime <- struct({time_struct})")

  time_float = time.mktime(time_struct)
  print(f"struct({time_struct}) -> time.mktime -> float({time_float})")

  time_struct = time.localtime(time_float)
  print(f"struct({time_struct}) <- time.localtime <- float({time_float})")

  time_milisecond = 1000000000001
  print(f"{time.localtime(time_milisecond / 1000)}")

  print(f"datetime min {datetime.min} max {datetime.max}")
  d = datetime.max
  print(f"{d.year} {d.month} {d.day} {d.hour} {d.minute} {d.second} {d.microsecond}")

  datetime_float = 1000000000.0
  datetime_tuple = datetime.fromtimestamp(datetime_float)
  print(f"float({datetime_float}) -> datetime.fromtimestamp -> datetime({datetime_tuple})")

  datetime_float = datetime_tuple.timestamp()
  print(f"float({datetime_float}) <- datetime.timestamp <- datetime({datetime_tuple})")

  datetime_str = time_str
  datetime_tuple = datetime.strptime(datetime_str, time_format)
  print(f"str({datetime_str}) -> datetime.strptime -> datetime({datetime_tuple})")

  datetime_float = datetime_tuple.strftime(time_format)
  print(f"str({datetime_float}) <- datetime.strftime <- datetime({datetime_tuple})")

  datetime_str = "1970-01-02 08:00:00"
  print(f"{datetime.strptime(datetime_str, time_format).timestamp()}")




if __name__ == "__main__":
  main()
