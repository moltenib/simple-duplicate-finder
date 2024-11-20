import json, os

settings = {}

def load_default_settings():
    settings['method'] = 1
    settings['path'] = os.path.expanduser('~')
    settings['font'] = ''
    settings['expand-one-row-at-once'] = False
    settings['expand-rows-as-inserted'] = True
    settings['scroll-to-inserted-rows'] = True
    settings['send-notifications'] = True
    settings['ask-before-deleting-one'] = True
    settings['ask-before-deleting-many'] = True
    settings['follow-symbolic-links'] = False
    settings['read-dotted-directories'] = False
    settings['read-dotted-files'] = False
    settings['limit'] = 0.0

if os.name == 'nt':
    settings_dir = os.path.expanduser('%LOCALAPPDATA%\\maun\\')
elif os.name == 'posix':
    settings_dir = os.path.expanduser('~/.config/maun/')
else:
    settings_dir = os.path.expanduser('~' + os.path.sep)

settings_file = settings_dir + 'maun.json'

if os.path.exists(settings_file):
    with open(settings_file, 'r') as f:
        settings = json.load(f)
else:
    if not os.path.isdir(settings_dir):
        os.makedirs(settings_dir)
    load_default_settings()

def save_settings():
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=4)
