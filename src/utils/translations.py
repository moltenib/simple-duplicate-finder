import gettext
import os

if os.name == 'nt':
    import winreg

else:
    import locale

def set_up_translations():
    if os.name == 'nt':
        key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\LanguagePack")
        try:
            language, _ = winreg.QueryValueEx(key, "Language")
            return language
        
        except FileNotFoundError:
            return None

        finally:
            winreg.CloseKey(key)

    else:
        language = locale.getlocale()

        if language:
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

