from datetime import datetime

def elapsed_time(time_started):
    elapsed = datetime.now() - time_started

    formatted_time = (datetime(1, 1, 1) + elapsed).strftime('%H:%M:%S')

    milliseconds = int(elapsed.microseconds / 1000)

    # Return time in this format: 00:00:00.000
    return f'{formatted_time}.{milliseconds:03d}'

