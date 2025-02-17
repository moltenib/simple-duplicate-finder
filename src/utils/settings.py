import json, os

class SettingsCopy:
    def __init__(self, dict_):
        for key, value in dict_.items():
            setattr(self, key, value)

class Settings:
    def __init__(self):
        self.load_default()

        self.file = self.find_settings_file()

        self.load()

    def load_default(self):
        self.method = 0
        self.paths = [os.path.expanduser('~'), None]
        self.font = ''
        self.theme = 'light'
        self.expand_one_row_at_once = False
        self.expand_rows_as_inserted = True
        self.scroll_to_inserted_rows = True
        self.ask_before_deleting_one = True
        self.ask_before_deleting_many = True
        self.follow_symbolic_links = False
        self.read_dotted_directories = False
        self.read_dotted_files = False
        self.limit = 50000

    def find_settings_file(self):
        if os.name == 'nt':
            settings_dir = os.path.join(
                os.environ.get('LOCALAPPDATA'),
                'simple-duplicate-finder')

        elif os.name == 'posix':
            settings_dir = os.path.expanduser(
                    '~/.config/simple-duplicate-finder')

        else:
            settings_dir = os.path.expanduser('~')

        return os.path.join(
                settings_dir,
                'settings.json')

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                settings = json.load(f)

            for key, value in settings.items():
                attr_name = key.replace('-', '_')
                if hasattr(self, attr_name):
                    setattr(self, attr_name, value)
        else:
            settings_dir = os.path.dirname(self.file)

            if not os.path.isdir(settings_dir):
                os.makedirs(settings_dir)

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    def copy(self):
        return SettingsCopy(self.__dict__.copy())

settings = Settings()

