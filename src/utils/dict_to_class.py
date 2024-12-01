class DictToClass:
    def __init__(self, dict_):
        for key, value in dict_.items():
            attr_name = key.replace('-', '_')
            setattr(self, attr_name, value)
