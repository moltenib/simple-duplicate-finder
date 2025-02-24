import os

from hashlib import sha1 as sha1_imported
from zlib import adler32 as adler32_imported
from datetime import datetime

### One function for each method

def sha1(file_):
    sum_ = sha1_imported()
    with open(file_, 'rb') as f:
        while True:
            # Number is equal to the buffer size in bytes
            # Read in chunks of 4 MB
            data = f.read(4194304)
            if not data:
                break
            sum_.update(data)
    return sum_.hexdigest()

def adler32(file_):
    sum_ = 0
    with open(file_, 'rb') as f:
        while True:
            data = f.read(4194304)
            if not data:
                break
            sum_ = adler32_imported(data, sum_)
    # Limit it to the last 32 bits (length of the checksum)
    return '%x' % (sum_ & 0xffffffff)

def modification_time(file_):
    return datetime.fromtimestamp(
            os.path.getmtime(file_)).isoformat(sep=' ')

