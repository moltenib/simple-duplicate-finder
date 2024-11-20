import os
from hashlib import sha1
from zlib import adler32

class Copying:
    app_name = 'Maun'
    image_file = os.path.dirname(os.path.abspath(__file__)) + \
            os.path.sep + 'art.png'
    version = 'alpha'
    app_comment = 'A simple program to help you find duplicates'
    copyright = '© 2018-2019 Bruno Molteni'
    website = 'https://github.com/stamby/maun'
    website_label = 'Website'
    licence_type = 3 # GPL 

### OS-related functions, return True if successful

class AppAndOs:
    def open_in_os(file_or_dir):
        if os.name == 'nt':
            return os.system('explorer.exe "' + file_or_dir + '"') == 0
        elif os.name == 'posix':
            if '\'' in file_or_dir:
                quote_char = '"'
            else:
                quote_char = '\''
            return os.system(
                    'xdg-open ' + quote_char + file_or_dir + quote_char) == 0 
        return False

    def chdir(dir_):
        os.chdir(dir_)

    def is_dir(dir_):
        return os.path.isdir(dir_)

    def is_file(file_):
        return os.path.isfile(file_)

    def is_link(file_):
        return os.path.islink(file_)

    def list_current_dir():
        return os.listdir('.')

    def abspath(file_or_dir):
        return os.path.abspath(file_or_dir)

    def dir_perms_OK(dir_):
        return os.access(dir_, os.R_OK and os.X_OK)

    def file_perms_R_OK(file_):
        return os.access(file_, os.R_OK)

    def file_perms_W_OK(file_):
        return os.access(file_, os.W_OK)

    def file_remove(file_):
        if os.access(file_, os.W_OK):
            os.remove(file_)
            return True
        return False

    def file_move(file_, file_or_dir):
        if ((os.path.isdir(file_or_dir)
        and not os.access(file_or_dir, os.W_OK))
        or (os.path.isfile(file_or_dir)
        and not os.access(os.path.dirname(file_or_dir), os.W_OK))):
            return False
        if os.name == 'nt':
            os.system(
                    'move "' + file_  + '" "' + file_or_dir + '"')
            return True
        elif os.name == 'posix':
            if '\'' in file_:
                quote_char = '"'
            else:
                quote_char = '\''
            return os.system(
                    'mv ' + quote_char + file_ + quote_char
                    + quote_char + file_or_dir + quote_char) == 0
        return False

    def notify_os(message_):
        if os.name == 'posix':
            if '\'' in message_:
                quote_char = '"'
            else:
                quote_char = '\''
            return os.system('notify-send' +
                ' -i ' + quote_char + Copying.image_file + quote_char +
                ' -a ' + quote_char +
                'Maun' + quote_char + ' ' + 'Maun' +
                ' ' + quote_char + message_ + quote_char) == 0
        return False

    def get_pretty_name(file_or_dir):
        name = file_or_dir.split(os.path.sep)
        if len(name) > 2:
            return '...' + os.path.sep + name[-2] + os.path.sep + name[-1]
        else:
            return file_or_dir

### Math, one function for each method

class AppMath:
    def sha1(file_):
        sum_ = sha1()
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
                sum_ = adler32(data, sum_)
        return '%x' % (sum_ & 0xffffffff)

    def size(file_):
        return '%x' % os.path.getsize(file_)
