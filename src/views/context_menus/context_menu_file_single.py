import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from utils import os_functions

class ContextMenuFileSingle(Gtk.Menu):
    def __init__(self, parent):
        Gtk.Menu.__init__(self, parent=parent)

        open_option = Gtk.MenuItem(
                label=_('Open')
        open_dir_option = Gtk.MenuItem(
                label=_('Open the containing directory')
        rename_option = Gtk.MenuItem(
                label=_('Rename')
        delete_option = Gtk.MenuItem(
                label=_('Delete')

class ContextMenuFileMultiple(Gtk.Menu):
    def __init__(self, parent):
        Gtk.Menu.__init__(self, parent=parent)

        select_oldest_option = Gtk.MenuItem(
                label=_('Select the oldest')
        # Only if there are two of them
        swap_names_option = Gtk.MenuItem(
                label=_('Swap names')
        bulk_rename_option = Gtk.MenuItem(
                label=_('Bulk rename')
        delete_selected_option = Gtk.MenuItem(
                label=_('Delete selected')

    #### TODO: MOVE THEM TO A HIGHER-LEVEL WIDGET
    def on_open_option(self, widget, ev):
        pass

    def on_open_dir_option(self, widget, ev):
        pass

    def on_rename_option(self, widget, ev):
        pass

    def on_delete_option(self, widget, ev):
        pass

