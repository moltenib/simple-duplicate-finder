from settings import (
        load_default_settings,
        settings as AppSettings)
import labels as AppLabels
from strictly_gobject_related import Gtk
from not_gui import Copying

class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent=None):
        Gtk.AboutDialog.__init__(self,
                title=AppLabels.ABOUT,
                parent=parent,
                version=Copying.version,
                comments=Copying.app_comment,
                copyright=Copying.copyright,
                website=Copying.website)
        self.set_program_name(Copying.app_name)
        self.set_license_type(Copying.licence_type)
        self.set_website_label(Copying.website_label)
        logo_pixbuf = self.get_logo().scale_simple(128, 128, 0)
        self.set_logo(logo_pixbuf)
        self.set_resizable(False)

class SettingsWindow(Gtk.Window):
    def __init__(self, parent=None):
        Gtk.Window.__init__(
                self, title=AppLabels.SETTINGS, resizable=False)
        self.set_border_width(6)
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_type_hint(1)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.set_destroy_with_parent(True)
        self.parent = parent

        # Interface
        self.expand_rows_as_inserted_button = Gtk.CheckButton(
                label=AppLabels.EXPAND_ROWS_AS_INSERTED)
        self.scroll_to_inserted_rows_button = Gtk.CheckButton(
                label=AppLabels.SCROLL_TO_INSERTED_ROWS)
        self.expand_one_row_at_once_button = Gtk.CheckButton(
                label=AppLabels.EXPAND_ONE_ROW_AT_ONCE)
        self.send_notifications_button = Gtk.CheckButton(
                label=AppLabels.SEND_NOTIFICATIONS)

        interface_vbox = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL, spacing=6)
        interface_vbox.set_border_width(6)
        interface_vbox.pack_start(
                self.expand_one_row_at_once_button, False, True, 0)
        interface_vbox.pack_start(
                self.expand_rows_as_inserted_button, False, True, 0)
        interface_vbox.pack_start(
                self.scroll_to_inserted_rows_button, False, True, 0)
        interface_vbox.pack_start(
                self.send_notifications_button, False, True, 0)

        interface_frame = Gtk.Frame(label=AppLabels.INTERFACE)
        interface_frame.add(interface_vbox)

        # Ask before deleting
        self.ask_file_one = Gtk.CheckButton(
                label=AppLabels.ASK_BEFORE_DELETING_ONE)
        self.ask_file_many = Gtk.CheckButton(
                label=AppLabels.ASK_BEFORE_DELETING_MANY)

        ask_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        ask_vbox.set_border_width(6)
        ask_vbox.pack_start(self.ask_file_one, False, True, 0)
        ask_vbox.pack_start(self.ask_file_many, False, True, 0)

        ask_frame = Gtk.Frame(label=AppLabels.ASK_BEFORE_DELETING)
        ask_frame.add(ask_vbox)

        # Behaviour
        self.follow_links_button = Gtk.CheckButton( 
                label=AppLabels.FOLLOW_LINKS)

        self.read_dotted_directories_button = Gtk.CheckButton(
                label=AppLabels.READ_DOTTED_DIRECTORIES)
        self.read_dotted_files_button = Gtk.CheckButton(
                label=AppLabels.READ_DOTTED_FILES)

        self.file_limit_button = Gtk.CheckButton(
                label=AppLabels.FILE_LIMIT)
        self.file_limit_spinbutton = Gtk.SpinButton.new_with_range(
                0.0, 999999.0, 1.0)
        self.file_limit_spinbutton.set_digits(0)
        self.file_limit_spinbutton.set_value(AppSettings['limit'])
        file_limit_hbox = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        file_limit_hbox.pack_start(self.file_limit_button, True, True, 0)
        file_limit_hbox.pack_start(self.file_limit_spinbutton, False, True, 0)

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

        behaviour_frame = Gtk.Frame(label=AppLabels.BEHAVIOUR)
        behaviour_frame.add(behaviour_vbox)

        hbox_top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox_top.pack_start(interface_frame, False, True, 0)
        hbox_top.pack_start(ask_frame, True, True, 0)

        about_button = Gtk.Button(
            label=AppLabels.ABOUT)
        load_default_button = Gtk.Button(
            label=AppLabels.LOAD_DEFAULT_SETTINGS)

        hbox_bottom = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
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
        self.send_notifications_button.connect(
                'toggled', self.on_send_notifications_toggled)

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
                AppSettings['expand-rows-as-inserted'])
        self.scroll_to_inserted_rows_button.set_active(
                AppSettings['scroll-to-inserted-rows'])
        self.expand_one_row_at_once_button.set_active(
                AppSettings['expand-one-row-at-once'])
        self.send_notifications_button.set_active(
                AppSettings['send-notifications'])
        self.ask_file_one.set_active(AppSettings['ask-before-deleting-one'])
        self.ask_file_many.set_active(AppSettings['ask-before-deleting-many'])
        self.follow_links_button.set_active(
                AppSettings['follow-symbolic-links'])
        self.read_dotted_directories_button.set_active(
                AppSettings['read-dotted-directories'])
        self.read_dotted_files_button.set_active(
                AppSettings['read-dotted-files'])
        if AppSettings['limit'] == 0:
            self.file_limit_button.set_active(False)
            self.file_limit_spinbutton.set_sensitive(False)
        else:
            self.file_limit_button.set_active(True)
            self.file_limit_spinbutton.set_sensitive(True)
        self.file_limit_spinbutton.set_value(AppSettings['limit'])

        self.parent.method_combo.set_active(
                AppSettings['method'])
        self.parent.folder_button.set_filename(
                AppSettings['path'])

    def on_expand_one_row_at_once_toggled(self, button):
        AppSettings['expand-one-row-at-once'] = button.get_active()

    def on_expand_rows_as_inserted_toggled(self, button):
        AppSettings['expand-rows-as-inserted'] = button.get_active()

    def on_scroll_to_inserted_toggled(self, button):
        AppSettings['scroll-to-inserted-rows'] = button.get_active()

    def on_send_notifications_toggled(self, button):
        AppSettings['send-notifications'] = button.get_active()

    def on_ask_file_one_toggled(self, button):
        AppSettings['ask-before-deleting-one'] = button.get_active()

    def on_ask_file_many_toggled(self, button):
        AppSettings['ask-before-deleting-many'] = button.get_active()

    def on_follow_links_toggled(self, button):
        AppSettings['follow-symbolic-links'] = button.get_active()

    def on_read_dotted_directories_toggled(self, button):
        AppSettings['read-dotted-directories'] = button.get_active()

    def on_read_dotted_files_toggled(self, button):
        AppSettings['read-dotted-files'] = button.get_active()

    def on_file_limit_toggled(self, button):
        if button.get_active():
            self.file_limit_spinbutton.set_sensitive(True)
            self.file_limit_spinbutton.grab_focus()
        else:
            self.file_limit_spinbutton.set_sensitive(False)
            self.file_limit_spinbutton.set_value(0)

    def on_file_limit_changed(self, button):
        AppSettings['limit'] = button.get_value_as_int()

    def on_about_clicked(self, button):
        self.destroy()
        dialog = AboutDialog(parent=self.parent)
        dialog.run()
        dialog.destroy()

    def on_load_default_clicked(self, button):
        load_default_settings()
        self.load_settings()

    def on_key_press(self, window, ev):
        if ev.keyval == 65307:
            self.destroy()
