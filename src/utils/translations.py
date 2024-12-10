import gettext
import locale
import os

if os.name == 'nt':
    import ctypes, sys

def set_up_translations():
    # Get the language string (two characters)
    if os.name == 'nt':
        lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()

        try:
            language = locale.windows_locale[lcid][:2]

        except:
            # Default to English (Windows)
            language = 'en'

    else:
        language = locale.getlocale()

        # Default to English (Linux, others)
        language = language[0][:2] if language else 'en'

    # Get the locale path (gettext)
    if os.name == 'nt' and hasattr(sys, '_MEIPASS'):
        locale_path = os.path.join(
            sys._MEIPASS,
            'resources',
            'locales')
        
    else:
        locale_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'resources',
            'locales')

    # Set up gettext
    gettext.bindtextdomain('messages', locale_path)
    gettext.textdomain('messages')

    try:
        # Look for the specified language
        translation = gettext.translation(
                'messages',
                localedir=locale_path,
                languages=[language])

        translation.install()

    except FileNotFoundError:
        # Default
        gettext.install('messages', localedir=locale_path)
