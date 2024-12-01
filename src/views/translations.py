import gettext
import locale
import os

def set_up_translations():
    # Choose the system locale, if available
    language = locale.getlocale()[0][:2]

    locale_path = os.path.join(
            os.path.dirname(__file__),
            '../../resources/locales')

    gettext.bindtextdomain('messages', locale_path)
    gettext.textdomain('messages')

    try:
        translation = gettext.translation(
                'messages', localedir=locale_path, languages=[language])

        translation.install()

    except FileNotFoundError:
        gettext.install('messages', localedir=locale_path)
        print("Defaulting to English translations")


