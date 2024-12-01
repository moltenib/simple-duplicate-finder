import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from threading import Thread

from utils.settings import settings
from utils import os_functions
from controllers.blocking import AppStatus, messy_code_block
from views.gui_widgets import TreeModel, TreeView
from views.gui_windows import SettingsWindow
from views import gui_queue as AppQueue

from gettext import gettext as _

import os

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=_('Simple Duplicate Finder'))

        logo_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '../../resources/icons/app_icon.png')

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_icon_from_file(
                logo_path)
        self.set_size_request(800, 600)
        self.set_border_width(6)

        self.method_combo = Gtk.ComboBoxText()
        for method in ('SHA-1', 'Adler-32', 'File size', 'File name'):
            self.method_combo.append_text(
                    _(method))

        self.method_combo.set_active(settings['method'])

        self.folder_button = Gtk.FileChooserButton(
                action=Gtk.FileChooserAction.SELECT_FOLDER,
                title=_('Choose path'))
        self.folder_button.set_filename(settings['path'])

        self.start_button = Gtk.Button(
                label=_('Start'))
        self.start_button.set_size_request(75, 0)

        settings_image = Gtk.Image(
                pixbuf=Gtk.IconTheme.get_default().load_icon(
                    'preferences-system', 16,
                    Gtk.IconLookupFlags.FORCE_SIZE))
        self.settings_button = Gtk.Button(image=settings_image)

        self.hash_tree_model = TreeModel()
        self.hash_tree_view = TreeView()
        self.hash_tree_view.set_model(self.hash_tree_model)

        hash_tree_selection = self.hash_tree_view.get_selection()

        hash_tree_scrolled = Gtk.ScrolledWindow()
        hash_tree_scrolled.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        hash_tree_scrolled.add(self.hash_tree_view)

        self.status_bar = Gtk.Statusbar()

        # Pack everything in boxes

        top_hbox = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=6)
        top_hbox.pack_start(self.method_combo, False, True, 0)
        top_hbox.pack_start(self.folder_button, True, True, 0)
        top_hbox.pack_start(self.settings_button, False, True, 0)
        top_hbox.pack_end(self.start_button, False, True, 0)

#        middle_right_vbox = Gtk.Box(
#                orientation=Gtk.Orientation.HORIZONTAL,
#                spacing=6)
#        middle_right_vbox.pack_start(Gtk.Image(), True, True, 0)

        middle_hbox = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=6)
        middle_hbox.pack_start(hash_tree_scrolled, True, True, 0)
#        middle_hbox.pack_end(middle_right_vbox, False, True, 0)

        vbox = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=6)
        vbox.pack_start(top_hbox, False, True, 0)
        vbox.pack_start(middle_hbox, True, True, 0)
        vbox.pack_end(self.status_bar, False, True, 0)

        self.add(vbox)

        # Change GUI behaviour

        self.method_combo.connect(
                'changed', self.on_method_changed)
        self.folder_button.connect(
                'file-set', self.on_folder_set)
        self.settings_button.connect(
                'clicked', self.on_settings_button_click)
        self.start_button.connect(
                'clicked', self.on_start_button_click)
        self.hash_tree_model.connect(
                'row-inserted', self.on_row_inserted)
        self.hash_tree_view.connect(
                'row-activated', self.on_row_activated)

        self.connect(
                'key-press-event', self.on_key_press)
        self.connect(
                'destroy', self.on_destruction)

        self.status_bar.push(1, _('To begin, please choose a directory from the top bar.'))

        self.start_button.grab_focus()

        self.thread = None
        self.started = False
        self.idle_source = 0

    def thread_start(self):
        self.thread = Thread(
                name='worker-thread',
                target=messy_code_block,
                daemon=False,
                args=(settings.copy(), AppQueue.signal_handler))
        self.thread.start()

    def thread_cancel(self):
        if self.thread is not None:
            AppStatus.cancelling = True
            self.thread.join()
            AppStatus.cancelling = False

    def gui_start(self):
        self.method_combo.set_sensitive(False)
        self.folder_button.set_sensitive(False)
        self.settings_button.set_sensitive(False)
        self.hash_tree_model.clear_all()
        self.hash_tree_view.columns_autosize()
        self.start_button.set_label(_('Cancel'))

    def gui_stop(self):
        self.start_button.set_label(_('Start'))
        self.settings_button.set_sensitive(True)
        self.folder_button.set_sensitive(True)
        self.method_combo.set_sensitive(True)

    def on_method_changed(self, combo):
        settings['method'] = combo.get_active()

    def on_folder_set(self, folder_button):
        settings['path'] = folder_button.get_filename()

    def start(self):
        self.gui_start()
        self.idle_source = GLib.idle_add(AppQueue.run, self)
        self.thread_start()
        self.started = True

    def cancel(self):
        self.thread_cancel()
        self.gui_stop()
        self.started = False

    def finish(self):
        self.started = False
        self.gui_stop()

    def on_settings_button_click(self, button):
        SettingsWindow(parent=self).show_all()

    def on_start_button_click(self, button):
        if not AppStatus.cancelling:
            if not self.started:
                self.start()
            else:
                self.cancel()

    def on_key_press(self, window, ev):
        # Escape
        if ev.keyval == 65307 and not AppStatus.cancelling:
            self.cancel()
            self.start_button.grab_focus()

        if ev.keyval == 65535 and not AppStatus.cancelling:
            if self.started:
                self.status_bar.push(1,
                        _('The search must be cancelled before deleting a file'))
                return

            rows = self.hash_tree_view.get_selection().get_selected_rows()

            if rows is None:
                return
            elif len(rows) > 1:
                # Get a list of files to delete, excluding hash rows
                selected_files = [self.hash_tree_model[row][0] for row in rows[1] if row.get_depth() == 2]
                # Get a list of iters to delete
                rows = [self.hash_tree_model.get_iter(row) for row in rows[1] if row.get_depth() == 2]

            if settings['ask-before-deleting-one'] and len(selected_files) == 1:
                dialog = Gtk.MessageDialog(
                        buttons=Gtk.ButtonsType.OK_CANCEL,
                        parent=self,
                        text=_('Are you sure you want to delete the following file?\n\n{}').format(selected_files[0]))

                response = dialog.run() == Gtk.ResponseType.OK

                dialog.destroy()
            elif settings['ask-before-deleting-many'] and len(selected_files) > 1:
                dialog = Gtk.MessageDialog(
                        buttons=Gtk.ButtonsType.OK_CANCEL,
                        parent=self,
                        text=_('Are you sure you want to delete the following files?\n\n{}').format(
                            '\n'.join(selected_files)))
    
                response = dialog.run() == Gtk.ResponseType.OK

                dialog.destroy()
            else:
                response = True

            if response == False:
                return

            i = 0

            while i < len(selected_files):
                if os_functions.file_remove(selected_files[i]):
                    parent = self.hash_tree_model.iter_parent(rows[i])

                    self.hash_tree_model.remove(rows[i])

                    if self.hash_tree_model.iter_n_children(parent) < 2:
                        self.hash_tree_model.remove(parent)

                    self.status_bar.push(1,
                            _('Files have been deleted'))

                i += 1

    def notify_os(self, message):
        if settings['send-notifications']:
            if not os_functions.notify_os(message):
                print(_('Error: routine \'{}\' has failed').format('send-notifications'))

    def on_row_inserted(self, model, path, iter_):
        if settings['expand-one-row-at-once']:
            self.hash_tree_view.collapse_all()
        if settings['expand-rows-as-inserted']:
            self.hash_tree_view.expand_to_path(path)
        if settings['scroll-to-inserted-rows']:
            self.hash_tree_view.scroll_to_cell(
                    path, None, False, 0.0, 0.0)

    def on_row_activated(self, tree_view, path, column):
        depth = path.get_depth()
        if depth == 1:
            row_was_expanded = tree_view.row_expanded(path)
            if settings['expand-one-row-at-once']:
                tree_view.collapse_all()
            if row_was_expanded:
                tree_view.collapse_row(path)
            else:
                tree_view.expand_row(path, False)
        elif depth == 2:
            iter_ = self.hash_tree_model.get_iter(path)
            file_ = self.hash_tree_model[iter_][0]
            if os_functions.open_in_os(file_):
                self.status_bar.push(1,
                    _('\'{}\' opened').format(
                        os_functions.get_pretty_name(file_)))
            else:
                self.status_bar.push(1,
                        _('\'{}\', {}, {} {}').format( # Name, type, size, size unit
                            os_functions.get_pretty_name(file_)))

    def on_destruction(self, window):
        AppQueue.destroy()
        self.thread_cancel()
