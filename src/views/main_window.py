import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gio', '2.0')
from gi.repository import GLib, Gio, Gtk

from controllers.blocking import blocking

from utils import os_functions
from utils.settings import settings

from views.main_window_tree import TreeModel, TreeView
from views.settings_window import SettingsWindow

from gettext import gettext as _

from datetime import datetime
import os

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=_('Simple Duplicate Finder'))

        # Define the logo
        logo_path = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)),
                    '../../resources/icons/app_icon.png')

        self.set_default_icon_from_file(
                logo_path)

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(800, 600)
        self.set_border_width(6)

        ## Top bar

        # Method combo

        self.method_combo = Gtk.ComboBoxText()

        for method in ('SHA-1', 'Adler-32', 'File size', 'File name'):
            self.method_combo.append_text(
                    _(method))

        self.method_combo.set_active(settings['method'])

        # Folder choosing button

        self.folder_button = Gtk.FileChooserButton(
                action=Gtk.FileChooserAction.SELECT_FOLDER,
                title=_('Choose path'))

        self.folder_button.set_filename(settings['path'])

        # Settings icon

        settings_image = Gtk.Image(
                pixbuf=Gtk.IconTheme.get_default().load_icon(
                    'preferences-system', 16,
                    Gtk.IconLookupFlags.FORCE_SIZE))

        self.settings_button = Gtk.Button(image=settings_image)

        # Start button

        self.start_button = Gtk.Button(
                label=_('Start'))

        self.start_button.set_size_request(75, 0)

        # Tree view

        self.hash_tree_model = TreeModel()
        self.hash_tree_view = TreeView(self.hash_tree_model)

        self.hash_tree_view.get_selection().connect(
                'changed', self.on_hash_tree_selection_changed)

        hash_tree_scrolled = Gtk.ScrolledWindow()
        hash_tree_scrolled.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        hash_tree_scrolled.add(self.hash_tree_view)

        # Status bar

        self.status_bar = Gtk.Statusbar()

        # Pack everything in boxes

        top_hbox = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=6)
        top_hbox.pack_start(self.method_combo, False, True, 0)
        top_hbox.pack_start(self.folder_button, True, True, 0)
        top_hbox.pack_start(self.settings_button, False, True, 0)
        top_hbox.pack_end(self.start_button, False, True, 0)

        middle_hbox = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=6)
        middle_hbox.pack_start(hash_tree_scrolled, True, True, 0)

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

        # Use GObject threading techniques
        self.task = None
        self.cancellable = None

        # Use this flag for GUI state changes
        self.started = False

    def on_method_changed(self, combo):
        settings['method'] = combo.get_active()

    def on_folder_set(self, folder_button):
        settings['path'] = folder_button.get_filename()

    def on_settings_button_click(self, button):
        SettingsWindow(parent=self).show_all()

    def on_start_button_click(self, button):
        if not self.started:
            self.start()
        else:
            self.cancel()

    def start(self):
        # GUI
        self.method_combo.set_sensitive(False)
        self.folder_button.set_sensitive(False)
        self.settings_button.set_sensitive(False)
        self.hash_tree_model.clear_all()
        self.hash_tree_view.columns_autosize()
        self.start_button.set_label(_('Cancel'))

        # Create a Gio.Cancellable and assign it to a Gio.Task
        self.cancellable = Gio.Cancellable()
        self.task = Gio.Task.new(None, self.cancellable, None)

        self.task.run_in_thread(
            # run_in_thread() expects a function with these parameters
            lambda task, source_object, task_data=None, cancellable=None:
                blocking(task, settings.copy(), self.handle_signal))

        self.started = True

    def cancel(self):
        # self.status_bar.push(1, _('Cancelling...'))

        # Cancel the Gio.Task
        self.cancellable.cancel()

        # Prepare the GUI to appear as "not started" again
        self.started = False

        # GUI
        self.gui_stop()

    def finish(self):
        self.started = False

        self.cancellable = None
        self.task = None

        # Same updates to the GUI as with self.cancel()
        self.gui_stop()

    def gui_stop(self):
        self.start_button.set_label(_('Start'))
        self.settings_button.set_sensitive(True)
        self.folder_button.set_sensitive(True)
        self.method_combo.set_sensitive(True)

    def on_key_press(self, window, ev):
        # Escape
        if ev.keyval == 65307:
            if self.started:
                self.cancel()

            else:
                self.hash_tree_view.get_selection().unselect_all()

            self.start_button.grab_focus()

        # Delete
        if ev.keyval == 65535:
            if self.started:
                self.status_bar.push(
                        1,
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
                        text=_(
                            'Are you sure you want to delete the following file?\n\n{}').format(
                                selected_files[0]))

                response = dialog.run() == Gtk.ResponseType.OK

                dialog.destroy()
            elif settings['ask-before-deleting-many'] and len(selected_files) > 1:
                dialog = Gtk.MessageDialog(
                        buttons=Gtk.ButtonsType.OK_CANCEL,
                        parent=self,
                        text=_(
                            'Are you sure you want to delete the following files?\n\n{}').format(
                            '\n'.join(selected_files)))
    
                response = dialog.run() == Gtk.ResponseType.OK

                dialog.destroy()

            else:
                response = True

            if not response:
                return

            i = 0

            while i < len(selected_files):
                if os_functions.file_remove(selected_files[i]):
                    parent = self.hash_tree_model.iter_parent(rows[i])

                    self.hash_tree_model.remove(rows[i])

                    # If the parent is out of children, remove the parent
                    if self.hash_tree_model.iter_n_children(parent) < 2:
                        self.hash_tree_model.remove(parent)

                    self.status_bar.push(1,
                            _('Files have been deleted'))

                i += 1

    def notify_os(self, message):
        if settings['send-notifications']:
            if not os_functions.notify_os(message):
                print(_('Error: routine \'{}\' has failed').format('send-notifications'))

    def on_hash_tree_selection_changed(self, hash_tree_selection):
        count = hash_tree_selection.count_selected_rows()

        if count == 0:
            self.status_bar.push(
                    1, _('Selection cleared').format(count))

        elif count == 1:
            row = hash_tree_selection.get_selected_rows()[1]
            row_content = self.hash_tree_model[row[0]][0]

            # If it is a file
            if row[0].get_depth() == 2:
                self.status_bar.push(1,
                        _("'{}'; modified on {}").format(
                            os_functions.get_pretty_name(row_content),
                            datetime.fromtimestamp(
                                os.path.getmtime(row_content)).strftime(
                                    '%Y-%m-%d, %H:%M:%S')))

            else:
                iter_ = self.hash_tree_model.get_iter(row[0])

                self.status_bar.push(1,
                        _("{} ({} files)").format(
                            row_content,
                            self.hash_tree_model.iter_n_children(iter_)))

        elif count > 1:
            self.status_bar.push(
                    1, _('{} rows selected').format(count))

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

        # Parent (code)
        if depth == 1:
            if settings['expand-one-row-at-once']:
                if tree_view.row_expanded(path):
                    tree_view.collapse_all()
                else:
                    # Any change to the tree makes all paths go obsolete
                    old_path_iter = self.hash_tree_model.get_iter(path)

                    tree_view.collapse_all()

                    new_path = self.hash_tree_model.get_path(old_path_iter)

                    tree_view.expand_row(new_path, False)

            elif tree_view.row_expanded(path):
                tree_view.collapse_row(path)

            else:
                tree_view.expand_row(path, False)

        # Child (file)
        elif depth == 2:
            # Get the file name from the tree view
            iter_ = self.hash_tree_model.get_iter(path)
            file_ = self.hash_tree_model[iter_][0]

            # Open the file
            if os_functions.open_in_os(file_):
                self.status_bar.push(1,
                    _('\'{}\' opened').format(
                        os_functions.get_pretty_name(file_)))

    def on_destruction(self, window):
        if self.started:
            self.cancel()

    def handle_signal(self, signal_name, *args):
        if signal_name == 'started':
            self.status_bar.push(1, _('Working...'))

        elif signal_name == 'append-parent':
            # This signal expects three arguments
            code, file_1, file_2 = args

            self.hash_tree_model.add_parent(code)
            self.hash_tree_model.add_child(code, file_1)
            self.hash_tree_model.add_child(code, file_2)

        elif signal_name == 'append-child':
            code, file_ = args

            self.hash_tree_model.add_child(code, file_)

        elif signal_name == 'cancelled':
            if self.task is None:
                return

            total_iterations, total_files = args

            message = _(
                    '{} repetitions found before cancelling; {} files processed').format(
                            total_iterations, total_files)

            self.notify_os(message)
            self.status_bar.push(1, message)
            self.cancel()

        elif signal_name == 'limit-reached':
            total_iterations, total_files = args

            message = _(
                    '{} repetitions found before reaching limit of {} files').format(
                            total_iterations, total_files)

            self.notify_os(message)
            self.status_bar.push(1, message)
            self.finish()

        elif signal_name == 'finished':
            total_iterations, total_files = args

            message = _('{} repetitions found within {} files').format(total_iterations, total_files)

            self.notify_os(message)
            self.status_bar.push(1, message)
            self.finish()

        elif signal_name == 'insufficient-permissions':
            item_dirname, item_basename = args

            message = _('Not enough permissions to open \'{}\'').format(
                    os.path.join(item_dirname, item_basename))
            self.status_bar.push(1, message)

        # Cancel the idle_add call
        return False

