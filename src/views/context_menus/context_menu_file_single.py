import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os

from utils import os_functions

class ContextMenuFileSingle(Gtk.Menu):
    def __init__(self, window, file_):
        Gtk.Menu.__init__(self)

        self.file = file_
        self.window = window

        open_option = Gtk.MenuItem(
                label=_('Open'))
        open_dir_option = Gtk.MenuItem(
                label=_('Open the containing directory'))
        rename_option = Gtk.MenuItem(
                label=_('Rename'))
        delete_option = Gtk.MenuItem(
                label=_('Delete'))

        self.attach(
                open_option,
                0, 1, 0, 1)

        self.attach(
                open_dir_option,
                0, 1, 2, 3)

        self.attach(
                rename_option,
                0, 1, 4, 5)

        self.attach(
                delete_option,
                0, 1, 6, 7)

        self.show_all()

        open_option.connect(
                'activate', self.on_open_option_activate)

        open_dir_option.connect(
                'activate', self.on_open_dir_option_activate)

        rename_option.connect(
                'activate', self.on_rename_option_activate)

        delete_option.connect(
                'activate', self.on_delete_option_activate)

    def on_open_option_activate(self, widget):
        self.window.open(self.file)

    def on_open_dir_option_activate(self, widget):
        pass

    def on_rename_option_activate(self, widget):
        pass

    def on_delete_option_activate(self, widget):
        window.delete_files_from_selection()

    def on_open_dir_option_activate(self, widget):
        pass

    def on_rename_option_activate(self, widget):
        pass

    def on_delete_option_activate(self, widget):
        pass

