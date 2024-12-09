import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gettext import gettext as _

class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self,
                title=_('About'),
                parent=parent,
                version='beta',
                comments=_('A program to find duplicates.'),
                copyright='© 2018, 2024 Bruno Molteni',
                website='https://github.com/moltenib/simple-duplicate-finder')
        self.set_program_name(_('Simple Duplicate Finder'))
        self.set_license_type(Gtk.License.GPL_3_0)
        logo_pixbuf = self.get_logo().scale_simple(128, 128, 0)
        self.set_logo(logo_pixbuf)
        self.set_resizable(False)

