import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from utils import os_functions

class ContextMenuFileMultiple(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        select_oldest_option = Gtk.MenuItem(
                label=_('Select the oldest'))
        # Only if there are two of them
        swap_names_option = Gtk.MenuItem(
                label=_('Swap names'))
        bulk_rename_option = Gtk.MenuItem(
                label=_('Bulk rename'))
        delete_selected_option = Gtk.MenuItem(
                label=_('Delete selected'))

        self.attach(
                select_oldest_option,
                0, 1, 0, 1)

        self.attach(
                swap_names_option,
                0, 1, 2, 3)

        self.attach(
                bulk_rename_option,
                0, 1, 4, 5)

        self.attach(
                delete_selected_option,
                0, 1, 6, 7)

        select_oldest_option.connect(
                'activate', self.on_select_oldest_option_activate)

        swap_names_option.connect(
                'activate', self.on_swap_names_option_activate)

        bulk_rename_option.connect(
                'activate', self.on_bulk_rename_option_activate)

        delete_selected_option.connect(
                'activate', self.on_delete_selected_option_activate)

        self.show_all()

    def on_select_oldest_option_activate(self, widget):
        pass

    def on_swap_names_option_activate(self, widget):
        pass

    def on_bulk_rename_option_activate(self, widget):
        pass

    def on_delete_selected_option_activate(self, widget):
        pass


