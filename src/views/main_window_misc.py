import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from utils.settings import settings

from datetime import datetime

class MethodCombo(Gtk.ComboBoxText):
    def __init__(self):
        Gtk.ComboBoxText.__init__(self)

        for method in (
                'SHA-1',
                'Adler-32',
                'Modif. time',
                'File name'):
            self.append_text(_(method))

        self.set_active(settings.method)

        self.set_tooltip_text(_('Method'))

class FolderButton(Gtk.FileChooserButton):
    def __init__(self):
        Gtk.FileChooserButton.__init__(
                self,
                action=Gtk.FileChooserAction.SELECT_FOLDER,
                title=_('Choose path'))

        self.set_filename(settings.paths[0])

        self.set_tooltip_text(_('Starting path'))

        # This avoids unnecessary space when loading it the first time
        self.show_all()

class SecondFolderButton(Gtk.FileChooserButton):
    def __init__(self):
        Gtk.FileChooserButton.__init__(
                self,
                action=Gtk.FileChooserAction.SELECT_FOLDER,
                title=_('Choose path'))

        none_button = Gtk.Button(label=_('(None)'))

        self.set_extra_widget(none_button)

        self.set_filename(settings.paths[0])

        self.set_tooltip_text(_('Starting path'))

        self.box.pack_start(none_button, True, True, 0)

        none_button.connect('clicked', self.on_none_button_clicked)

        self.show_all()

    def on_none_button_clicked(self, button):
        self.set_filename(None)

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

class ExportDialog(Gtk.FileChooserDialog):
    def __init__(self, parent):
        Gtk.FileChooserDialog.__init__(
                self,
                parent=parent,
                action=Gtk.FileChooserAction.SAVE,
                title=_('Export as CSV'),
                buttons=(
                    _('Cancel'), Gtk.ResponseType.CANCEL,
                    _('Save'), Gtk.ResponseType.ACCEPT),
                do_overwrite_confirmation=True)

        file_filter = Gtk.FileFilter()
        file_filter.set_name('Comma-Separated Values (CSV)')
        file_filter.add_pattern('*.csv')
        file_filter.add_mime_type('text/csv')

        self.add_filter(file_filter)

        self.set_current_name(
                '{}-{}.csv'.format(
                    _('Simple Duplicate Finder').replace(' ', '-'),
                    datetime.now().strftime(
                        '%Y-%m-%d-%H-%M-%S')))

class DeleteDialog(Gtk.MessageDialog):
    def __init__(self, parent, selected_files):
        Gtk.MessageDialog.__init__(
                self,
                parent=parent,
                buttons=Gtk.ButtonsType.OK_CANCEL)

        self.set_title(_('Confirm deletion'))

        if len(selected_files) == 1:
            self.set_markup(
                    _('Are you sure you want to delete the following file?')
                    + '\n\n<b>{}</b>'.format(selected_files[0]))

        else:
            self.set_markup(
                    _('Are you sure you want to delete the following files?')
                    + '\n\n·\t<b>{}</b>'.format(
                            '</b>\n·\t<b>'.join(selected_files)))
