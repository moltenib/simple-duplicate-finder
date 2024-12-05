import gettext
import os

if os.name == 'nt':
    import ctypes

else:
    import locale

def set_up_translations():
    if os.name == 'nt':
        lcid = ctypes.windll.kernel32.GetSystemDefaultUILanguage()

        if lcid in (
                1031, # German (Germany)
                3079, # German (Austria)
                2055, # German (Switzerland)
                4093, # German (Liechtenstein)
                4105): # German (Luxembourg)
            language = 'de'

        elif lcid in (
                1040, # Italian (Italy)
                2060): # Italian (Switzerland)
            language = 'it'

        elif lcid in (
                1046, # Portuguese (Brazil)
                2070, # Portuguese (Portugal)
                16394, # Portuguese (Angola)
                2006): # Portuguese (Mozambique)
            language = 'pt'

        elif lcid in (
                1036, # French (France)
                2060, # French (Belgium)
                3084, # French (Canada)
                4108, # French (Switzerland)
                5132, # French (Luxembourg)
                6156): # French (Monaco)
            language = 'fr'

        elif lcid in (
                1034, # Spanish (Spain - Traditional Sort)
                2058, # Spanish (Mexico)
                10250, # Spanish (Argentina)
                1026, # Spanish (Chile)
                9226, # Spanish (Colombia)
                1029, # Spanish (Peru)
                8202, # Spanish (Venezuela)
                14346, # Spanish (Uruguay)
                15370, # Spanish (Paraguay)
                16394, # Spanish (Bolivia)
                17418, # Spanish (Ecuador)
                4106, # Spanish (Guatemala)
                18442, # Spanish (Honduras)
                3082, # Spanish (El Salvador)
                5130, # Spanish (Costa Rica)
                6154, # Spanish (Panama)
                7178, # Spanish (Dominican Republic)
                8206, # Spanish (Nicaragua)
                10250, # Spanish (Mexico)
                1033): # Spanish (USA)
            language = 'es'

        else:
            language = 'en'

    else:
        language = locale.getlocale()

        if language:
            language = locale.getlocale()[0][:2]

    locale_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'resources',
            'locales')

    gettext.bindtextdomain('messages', locale_path)
    gettext.textdomain('messages')

    try:
        translation = gettext.translation(
                'messages', localedir=locale_path, languages=[language])

        translation.install()

    except FileNotFoundError:
        gettext.install('messages', localedir=locale_path)

