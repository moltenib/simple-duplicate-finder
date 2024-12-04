import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from utils.settings import settings

from gettext import gettext as _

class MethodCombo(Gtk.ComboBoxText):
    def __init__(self):
        Gtk.ComboBoxText.__init__(self)

        for method in (
                'SHA-1',
                'Adler-32',
                'Modif. time',
                'File name'):
            self.append_text(_(method))

        self.set_active(settings['method'])

        self.set_tooltip_text(_('Method'))

class FolderButton(Gtk.FileChooserButton):
    def __init__(self):
        Gtk.FileChooserButton.__init__(
                self,
                action=Gtk.FileChooserAction.SELECT_FOLDER,
                title=_('Choose path'))

        self.set_filename(settings['path'])

        self.set_tooltip_text(_('Starting path'))

class SettingsButton(Gtk.Button):
    def __init__(self):
        image = Gtk.Image(
                pixbuf=Gtk.IconTheme.get_default().load_icon(
                    'preferences-system', 16,
                    Gtk.IconLookupFlags.FORCE_SIZE))

        Gtk.Button.__init__(self, image=image)

        self.set_tooltip_text(_('Settings'))

class StartButton(Gtk.Button):
    def __init__(self):
        Gtk.Button.__init__(self, label=_('Start'))
        self.set_size_request(75, 0)

class ExportButton(Gtk.Button):
    def __init__(self):
        image = Gtk.Image(
                pixbuf=Gtk.IconTheme.get_default().load_icon(
                    'document-save', 16,
                    Gtk.IconLookupFlags.FORCE_SIZE))

        Gtk.Button.__init__(self, image=image)

        self.set_tooltip_text(_('Export as CSV'))

