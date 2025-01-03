#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from utils.settings import settings
from utils.translations import set_up_translations

from views.main_window import MainWindow

def main():
    if settings.theme == 'dark':
        Gtk.Settings = Gtk.Settings.get_default()
        Gtk.Settings.set_property(
                'gtk-application-prefer-dark-theme',
                True)

    set_up_translations()

    w = MainWindow()
    w.connect_after('destroy', Gtk.main_quit)
    w.show_all()
    Gtk.main()

    settings.save()

if __name__ == '__main__':
    main()

