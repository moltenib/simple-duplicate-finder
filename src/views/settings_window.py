import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from .about_dialog import AboutDialog
from utils.settings import settings

from os import name as os_name

class SettingsWindow(Gtk.Window):
    def __init__(self, parent):
        Gtk.Window.__init__(
                self, title=_('Settings'), resizable=False)

        self.set_border_width(6)
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.set_destroy_with_parent(True)
        self.parent = parent

        # Interface
        self.expand_rows_as_inserted_button = Gtk.CheckButton(
                label=_('Expand rows as they appear'))
        self.scroll_to_inserted_rows_button = Gtk.CheckButton(
                label=_('Scroll to inserted rows'))
        self.expand_one_row_at_once_button = Gtk.CheckButton(
                label=_('Expand one row at once'))

        theme_label = Gtk.Label(label=_('Theme:'))
        theme_label.set_xalign(0)
        self.theme_combo = Gtk.ComboBoxText()

        for theme in ('Light', 'Dark'):
            self.theme_combo.append_text(_(theme))

        interface_vbox = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL, spacing=6)
        interface_vbox.set_border_width(6)
        interface_vbox.pack_start(
                self.expand_one_row_at_once_button, False, True, 0)
        interface_vbox.pack_start(
                self.expand_rows_as_inserted_button, False, True, 0)

        interface_vbox.pack_start(
                self.scroll_to_inserted_rows_button, False, True, 0)

        if os_name == 'nt':
            theme_hbox = Gtk.Box(
                    orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

            theme_hbox.pack_start(
                    theme_label, True, True, 0)
            theme_hbox.pack_start(
                    self.theme_combo, True, True, 0)

            interface_vbox.pack_start(
                    theme_hbox, False, True, 0)

        interface_frame = Gtk.Frame(label=_('Interface'))
        interface_frame.add(interface_vbox)

        # Ask before deleting
        self.ask_file_one = Gtk.CheckButton(
                label=_('One file'))
        self.ask_file_many = Gtk.CheckButton(
                label=_('Multiple files'))

        ask_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        ask_vbox.set_border_width(6)
        ask_vbox.pack_start(self.ask_file_one, False, True, 0)
        ask_vbox.pack_start(self.ask_file_many, False, True, 0)

        ask_frame = Gtk.Frame(label=_('Ask before deleting'))
        ask_frame.add(ask_vbox)

        # Behaviour
        self.follow_links_button = Gtk.CheckButton( 
                label=_('Follow symbolic links'))

        self.read_dotted_directories_button = Gtk.CheckButton(
                label=_('Read dotted directories'))

        self.read_dotted_files_button = Gtk.CheckButton(
                label=_('Read dotted files'))

        self.file_limit_button = Gtk.CheckButton(
                label=_('Stop when a file limit is reached'))
        self.file_limit_spinbutton = Gtk.SpinButton.new_with_range(
                0.0, 999999.0, 1.0)
        self.file_limit_spinbutton.set_digits(0)
        self.file_limit_spinbutton.set_value(float(settings.limit))
        file_limit_hbox = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        file_limit_hbox.pack_start(
                self.file_limit_button, True, True, 0)
        file_limit_hbox.pack_start(
                self.file_limit_spinbutton, False, True, 0)

        behaviour_vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=6)
        behaviour_vbox.set_border_width(6)
        behaviour_vbox.pack_start(
            self.follow_links_button, True, True, 0)
        behaviour_vbox.pack_start(
            self.read_dotted_directories_button, True, True, 0)
        behaviour_vbox.pack_start(
            self.read_dotted_files_button, True, True, 0)
        behaviour_vbox.pack_start(
            file_limit_hbox, True, True, 0)

        behaviour_frame = Gtk.Frame(label=_('Behaviour'))
        behaviour_frame.add(behaviour_vbox)

        hbox_top = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox_top.pack_start(interface_frame, False, True, 0)
        hbox_top.pack_start(ask_frame, True, True, 0)

        about_button = Gtk.Button(
                label=_('About'))
        load_default_button = Gtk.Button(
                label=_('Load defaults'))

        hbox_bottom = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox_bottom.pack_start(about_button, False, False, 0)
        hbox_bottom.pack_start(load_default_button, False, False, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.pack_start(hbox_top, True, True, 0)
        vbox.pack_start(behaviour_frame, False, True, 0)
        vbox.pack_start(hbox_bottom, True, True, 0)

        self.add(vbox)

        self.load_settings()

        self.expand_one_row_at_once_button.connect(
                'toggled', self.on_expand_one_row_at_once_toggled)
        self.expand_rows_as_inserted_button.connect(
                'toggled', self.on_expand_rows_as_inserted_toggled)
        self.scroll_to_inserted_rows_button.connect(
                'toggled', self.on_scroll_to_inserted_toggled)

        if os_name == 'nt':
            self.theme_combo.connect(
                    'changed', self.on_theme_changed)

        self.ask_file_one.connect('toggled', self.on_ask_file_one_toggled)
        self.ask_file_many.connect('toggled', self.on_ask_file_many_toggled)

        self.follow_links_button.connect(
                'toggled', self.on_follow_links_toggled)
        self.read_dotted_directories_button.connect(
                'toggled', self.on_read_dotted_directories_toggled)
        self.read_dotted_files_button.connect(
                'toggled', self.on_read_dotted_files_toggled)
        self.file_limit_button.connect(
                'toggled', self.on_file_limit_toggled)
        self.file_limit_spinbutton.connect(
                'value-changed', self.on_file_limit_changed)

        about_button.connect(
                'clicked', self.on_about_clicked)
        load_default_button.connect(
                'clicked', self.on_load_default_clicked)

        self.connect('key-press-event', self.on_key_press)

    def load_settings(self):
        self.expand_rows_as_inserted_button.set_active(
                settings.expand_rows_as_inserted)
        self.scroll_to_inserted_rows_button.set_active(
                settings.scroll_to_inserted_rows)
        self.expand_one_row_at_once_button.set_active(
                settings.expand_one_row_at_once)
        self.theme_combo.set_active(
                1 if settings.theme == 'dark' else 0)
        self.ask_file_one.set_active(
                settings.ask_before_deleting_one)
        self.ask_file_many.set_active(
                settings.ask_before_deleting_many)
        self.follow_links_button.set_active(
                settings.follow_symbolic_links)
        self.read_dotted_directories_button.set_active(
                settings.read_dotted_directories)
        self.read_dotted_files_button.set_active(
                settings.read_dotted_files)

        if settings.limit == 0:
            self.file_limit_button.set_active(False)
            self.file_limit_spinbutton.set_sensitive(False)
        else:
            self.file_limit_button.set_active(True)
            self.file_limit_spinbutton.set_sensitive(True)

        self.file_limit_spinbutton.set_value(settings.limit)

        self.parent.method_combo.set_active(
                settings.method)
        self.parent.folder_button.set_filename(
                settings.paths[0])

        if settings.paths[1] is None:
            self.parent.second_folder_button.set_none()
            self.parent.remove_button.set_sensitive(False)

        else:
            self.parent.folder_button.set_filename(
                    settings.paths[1])

    def on_expand_one_row_at_once_toggled(self, button):
        settings.expand_one_row_at_once = button.get_active()

    def on_expand_rows_as_inserted_toggled(self, button):
        settings.expand_rows_as_inserted = button.get_active()

    def on_scroll_to_inserted_toggled(self, button):
        settings.scroll_to_inserted_rows = button.get_active()

    def on_ask_file_one_toggled(self, button):
        settings.ask_before_deleting_one = button.get_active()

    def on_ask_file_many_toggled(self, button):
        settings.ask_before_deleting_many = button.get_active()

    def on_follow_links_toggled(self, button):
        settings.follow_symbolic_links = button.get_active()

    def on_read_dotted_directories_toggled(self, button):
        settings.read_dotted_directories = button.get_active()

    def on_read_dotted_files_toggled(self, button):
        settings.read_dotted_files = button.get_active()

    def on_theme_changed(self, combo):
        dark = combo.get_active() == 1

        # Change the theme
        Gtk.Settings = Gtk.Settings.get_default()
        Gtk.Settings.set_property(
                'gtk-application-prefer-dark-theme',
                dark)

        settings.theme = 'dark' if dark else 'light'

    def on_file_limit_toggled(self, button):
        if button.get_active():
            self.file_limit_spinbutton.set_sensitive(True)
            self.file_limit_spinbutton.grab_focus()
        else:
            self.file_limit_spinbutton.set_sensitive(False)
            self.file_limit_spinbutton.set_value(0)

    def on_file_limit_changed(self, button):
        settings.limit = button.get_value_as_int()

    def on_about_clicked(self, button):
        self.destroy()
        dialog = AboutDialog(self.parent)
        dialog.run()
        dialog.destroy()

    def on_load_default_clicked(self, button):
        settings.load_default()

        self.load_settings()

    def on_key_press(self, window, ev):
        # Escape
        if ev.keyval == 65307:
            self.destroy()

