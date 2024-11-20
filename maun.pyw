#!/usr/bin/python3

from threading import Thread

import labels as AppLabels
from settings import settings as AppSettings, save_settings 
from strictly_gobject_related import Gtk, GLib
from blocking import AppStatus, messy_code_block
from gui_widgets import TreeModel, TreeView
from gui_windows import SettingsWindow
from not_gui import Copying, AppAndOs
import gui_queue as AppQueue

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=Copying.app_name)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_icon_from_file(Copying.image_file)
        self.set_size_request(800, 600)
        self.set_border_width(6)

        self.method_combo = Gtk.ComboBoxText()
        for method in AppLabels.AVAILABLE_METHODS:
            self.method_combo.append_text(method)
        self.method_combo.set_active(AppSettings['method'])

        self.folder_button = Gtk.FileChooserButton(
                action=Gtk.FileChooserAction.SELECT_FOLDER,
                title=AppLabels.CHOOSE_PATH)
        self.folder_button.set_filename(AppSettings['path'])

        self.start_button = Gtk.Button(
                label=AppLabels.START)
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

        self.status_bar.push(1, AppLabels.WELCOME)

        self.start_button.grab_focus()

        self.thread = None
        self.started = False
        self.idle_source = 0

    def thread_start(self):
        self.thread = Thread(
                name='worker-thread',
                target=messy_code_block,
                daemon=False,
                args=(AppSettings.copy(), AppQueue.signal_handler))
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
        self.start_button.set_label(AppLabels.CANCEL)

    def gui_stop(self):
        self.start_button.set_label(AppLabels.START)
        self.settings_button.set_sensitive(True)
        self.folder_button.set_sensitive(True)
        self.method_combo.set_sensitive(True)

    def on_method_changed(self, combo):
        AppSettings['method'] = combo.get_active()

    def on_folder_set(self, folder_button):
        AppSettings['path'] = folder_button.get_filename()

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
            rows = self.hash_tree_view.get_selection().get_selected_rows()

            if rows is None:
                return
            elif len(rows) > 1:
                # Get a list of files to delete, excluding hash rows
                selected_files = [self.hash_tree_model[row][0] for row in rows[1] if row.get_depth() == 2]
                # Get a list of iters to delete
                rows = [self.hash_tree_model.get_iter(row) for row in rows[1] if row.get_depth() == 2]

            if AppSettings['ask-before-deleting-one'] and len(selected_files) == 1:
                dialog = Gtk.MessageDialog(
                        buttons=Gtk.ButtonsType.OK_CANCEL,
                        parent=self,
                        text=AppLabels.CONFIRM_DELETION_ONE.format('\n'.join(selected_files)))

                response = dialog.run() == -5

                dialog.destroy()
            elif AppSettings['ask-before-deleting-many'] and len(selected_files) > 1:
                dialog = Gtk.MessageDialog(
                        buttons=Gtk.ButtonsType.OK_CANCEL,
                        parent=self,
                        text=AppLabels.CONFIRM_DELETION_MANY.format(
                            '\n'.join(selected_files)))
    
                response = dialog.run() == -5

                dialog.destroy()
            else:
                response = True

            if response == False:
                return

            i = 0

            while i < len(selected_files):
                if AppAndOs.file_remove(selected_files[i]):
                    parent = self.hash_tree_model.iter_parent(rows[i])

                    self.hash_tree_model.remove(rows[i])

                    if self.hash_tree_model.iter_n_children(parent) < 2:
                        self.hash_tree_model.remove(parent)

                    self.status_bar.push(1,
                            AppLabels.FILES_DELETED)

                i += 1

    def notify_os(self, message):
        if AppSettings['send-notifications']:
            if not AppAndOs.notify_os(message):
                print(AppLabels.ROUTINE_FAILED.format('send-notifications'))

    def on_row_inserted(self, model, path, iter_):
        if AppSettings['expand-one-row-at-once']:
            self.hash_tree_view.collapse_all()
        if AppSettings['expand-rows-as-inserted']:
            self.hash_tree_view.expand_to_path(path)
        if AppSettings['scroll-to-inserted-rows']:
            self.hash_tree_view.scroll_to_cell(
                    path, None, False, 0.0, 0.0)

    def on_row_activated(self, tree_view, path, column):
        depth = path.get_depth()
        if depth == 1:
            row_was_expanded = tree_view.row_expanded(path)
            if AppSettings['expand-one-row-at-once']:
                tree_view.collapse_all()
            if row_was_expanded:
                tree_view.collapse_row(path)
            else:
                tree_view.expand_row(path, False)
        elif depth == 2:
            iter_ = self.hash_tree_model.get_iter(path)
            file_ = self.hash_tree_model[iter_][0]
            if AppAndOs.open_in_os(file_):
                self.status_bar.push(1,
                    AppLabels.FILE_OPENED.format(
                        AppAndOs.get_pretty_name(file_)))
            else:
                self.status_bar.push(1,
                        AppLabels.FILE_NOT_OPENED.format(
                            AppAndOs.get_pretty_name(file_)))

    def on_destruction(self, window):
        AppQueue.destroy()
        self.thread_cancel()

w = MainWindow()
w.connect_after('destroy', Gtk.main_quit)
w.show_all()
Gtk.main()
save_settings()
