import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from utils import os_functions

class ContextMenuCodeSingle(Gtk.Menu):
    def __init__(self, tree_view):
        Gtk.Menu.__init__(self)

        self.tree_view = tree_view

        expand_all_option = Gtk.MenuItem(
                label=_('Expand all'))

        collapse_all_option = Gtk.MenuItem(
                label=_('Collapse all'))

        self.attach(
                expand_all_option,
                0, 1, 0, 1)

        self.attach(
                collapse_all_option,
                0, 1, 2, 3)

        expand_all_option.connect(
                'activate', self.on_expand_all_activate)

        collapse_all_option.connect(
                'activate', self.on_collapse_all_activate)

        self.show_all()

    def on_expand_all_activate(self, widget):
        self.tree_view.expand_all()

    def on_collapse_all_activate(self, widget):
        self.tree_view.collapse_all()

