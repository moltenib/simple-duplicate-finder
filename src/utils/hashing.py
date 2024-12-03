import os

from hashlib import sha1 as sha1_imported
from zlib import adler32 as adler32_imported

### One function for each method

def sha1(file_):
    sum_ = sha1_imported()
    with open(file_, 'rb') as f:
        while True:
            # Number is equal to the buffer size in bytes
            data = f.read(4096)
            if not data:
                break
            sum_.update(data)
    return sum_.hexdigest()

def adler32(file_):
    sum_ = 0
    with open(file_, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            sum_ = adler32_imported(data, sum_)
    return '%x' % (sum_ & 0xffffffff)

def modification_time(file_):
    return os.path.getmtime(file_)

