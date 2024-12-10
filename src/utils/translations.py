import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gettext
import os

if os.name == 'nt':
    import ctypes, locale, sys

def set_up_translations():
    # Get the language string (two characters)
    if os.name == 'nt':
        lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()

        try:
            language = locale.windows_locale[lcid][:2]

        except:
            language = 'en'

    else:
        language = locale.getlocale()

        if language:
            language = language[0][:2]

    # Get the locale path (gettext)
    if hasattr(sys, '_MEIPASS'):
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
        translation = gettext.translation(
                'messages',
                localedir=locale_path,
                languages=[language],
                fallback=False)

        translation.install()

    except FileNotFoundError:
        gettext.install('messages', localedir=locale_path)
