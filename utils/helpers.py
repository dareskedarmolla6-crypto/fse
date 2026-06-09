import datetime

def log(message):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time_stamp}] {message}")
