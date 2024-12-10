import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gio', '2.0')
from gi.repository import GLib, Gio, Gtk

from controllers.blocking import blocking

from utils import os_functions
from utils.settings import settings

from views.main_window_misc import *
from views.main_window_tree import TreeModel, TreeView
from views.settings_window import SettingsWindow

from datetime import datetime
import os, sys

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=_('Simple Duplicate Finder'))

        # Define the logo path
        # Running under MSYS2
        if hasattr(sys, '_MEIPASS'):
            logo_path = os.path.join(
                    sys._MEIPASS,
                    'resources',
                    'icons',
                    'app_icon.png')

        # Linux or Unix-based
        else:
            logo_path = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)),
                    '..',
                    '..',
                    'resources',
                    'icons',
                    'app_icon.png')

        self.set_default_icon_from_file(
                logo_path)

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(800, 600)
        self.set_border_width(6)

        ## Top bar

        self.method_combo = MethodCombo()

        self.folder_button = FolderButton()

        self.settings_button = SettingsButton()

        self.start_button = StartButton()

        # Tree view

        self.hash_tree_model = TreeModel()
        self.hash_tree_view = TreeView(self.hash_tree_model)

        hash_tree_scrolled = Gtk.ScrolledWindow()
        hash_tree_scrolled.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        hash_tree_scrolled.add(self.hash_tree_view)

        # Status bar

        self.status_bar = Gtk.Statusbar()

        # Export button

        self.export_button = ExportButton()

        # TODO: Add CSV import
        self.export_button.set_sensitive(False)

        # Pack everything in boxes

        top_hbox = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=6)
        top_hbox.pack_start(
                self.method_combo, False, True, 0)
        top_hbox.pack_start(
                self.folder_button, True, True, 0)
        top_hbox.pack_start(
                self.settings_button, False, True, 0)
        top_hbox.pack_end(
                self.start_button, False, True, 0)

        middle_hbox = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=6)
        middle_hbox.pack_start(
                hash_tree_scrolled, True, True, 0)

        bottom_hbox = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=6)
        bottom_hbox.pack_start(
                self.status_bar, True, True, 0)
        bottom_hbox.pack_end(
                self.export_button, False, True, 0)

        vbox = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=6)
        vbox.pack_start(
                top_hbox, False, True, 0)
        vbox.pack_start(
                middle_hbox, True, True, 0)
        vbox.pack_end(
                bottom_hbox, False, True, 0)

        self.add(vbox)

        # Change GUI behaviour

        self.method_combo.connect(
                'changed', self.on_method_changed)
        self.folder_button.connect(
                'file-set', self.on_folder_set)
        self.settings_button.connect(
                'clicked', self.on_settings_button_clicked)
        self.start_button.connect(
                'clicked', self.on_start_button_clicked)
        self.hash_tree_model.connect(
                'row-inserted', self.on_row_inserted)
        self.hash_tree_view.connect(
                'row-activated', self.on_row_activated)

        self.hash_tree_view.get_selection().connect(
                'changed', self.on_hash_tree_selection_changed)

        self.export_button.connect(
                'clicked', self.on_export_button_clicked)

        self.connect(
                'key-press-event', self.on_key_press)
        self.connect(
                'destroy', self.on_destruction)

        self.status_bar.push(
                1,
                _('To begin, please choose a directory from the top bar.'))

        self.start_button.grab_focus()

        # Use GObject threading techniques
        self.task = None
        self.cancellable = None

        # Use this flag for GUI state changes
        self.started = False

    def on_method_changed(self, combo):
        settings.method = combo.get_active()

    def on_folder_set(self, folder_button):
        settings.path = folder_button.get_filename()

    def on_settings_button_clicked(self, button):
        SettingsWindow(self).show_all()

    def on_start_button_clicked(self, button):
        if not self.started:
            self.start()
        else:
            self.cancellable.cancel()

    def on_export_button_clicked(self, button):
        dialog = ExportDialog(self)

        if dialog.run() == Gtk.ResponseType.ACCEPT:
            file_name = dialog.get_filename()

            if not file_name.lower().endswith('.csv'):
                file_name += '.csv'
            
            self.hash_tree_model.print_to_file(file_name)

            self.status_bar.push(
                    1,
                    _("Exported to '{}'").format(file_name))

        dialog.destroy()

    def start(self):
        # GUI
        self.method_combo.set_sensitive(False)
        self.folder_button.set_sensitive(False)
        self.settings_button.set_sensitive(False)
        self.export_button.set_sensitive(False)
        self.hash_tree_model.clear_all()
        self.hash_tree_view.columns_autosize()
        self.start_button.set_label(_('Cancel'))

        # Create a Gio.Cancellable and assign it to a Gio.Task
        self.cancellable = Gio.Cancellable()
        self.task = Gio.Task.new(None, self.cancellable, self.on_task_finished)

        self.task.run_in_thread(
                lambda task, source_object, task_data=None, cancellable=None:
                    blocking(task, settings.copy(), self.handle_signal))

        self.started = True

    def on_task_finished(self, *args):
        self.started = False

        self.cancellable = None
        self.task = None

        self.method_combo.set_sensitive(True)
        self.folder_button.set_sensitive(True)
        self.settings_button.set_sensitive(True)
        self.start_button.set_label(_('Start'))

        if self.hash_tree_model.get_iter_first():
            self.export_button.set_sensitive(True)

        self.start_button.grab_focus()

    def on_key_press(self, window, ev):
        # Escape
        if ev.keyval == 65307:
            if self.started:
                self.cancellable.cancel()

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

            model, rows = self.hash_tree_view.get_selection().get_selected_rows()

            if len(rows) == 0:
                return

            selected_files = []
            iters_to_delete = []

            for row in rows:
                # Populate the list of files and rows to delete
                # excluding parents
                if row.get_depth() == 2:
                    selected_files.append(model[row][0])

                    iters_to_delete.append(model.get_iter(row))

            if settings.ask_before_deleting_one \
                    and len(selected_files) == 1 \
                    or settings.ask_before_deleting_many \
                    and len(selected_files) > 1:
                dialog = DeleteDialog(self, selected_files)

                response = dialog.run() == Gtk.ResponseType.OK

                dialog.destroy()

            else:
                response = True

            if not response:
                return

            i = 0
            parents_to_remove = set()
            deleted = False

            while i < len(iters_to_delete):
                # Delete the file
                if os_functions.file_remove(selected_files[i]):
                    # Get the parent
                    parent = model.iter_parent(iters_to_delete[i])

                    # If the parent has two children, flag it for removal
                    # Using '==' and not '<=' because we do not to add it
                    # twice when reaching one child
                    if model.iter_n_children(parent) == 2:
                        parents_to_remove.add(parent)

                    # Delete the child
                    model.remove(iters_to_delete[i])

                    i += 1

            if deleted:
                self.status_bar.push(1,
                        _('Files have been deleted'))

            for parent in parents_to_remove:
                self.hash_tree_model.remove(parent)

    def on_hash_tree_selection_changed(self, hash_tree_selection):
        model, rows = hash_tree_selection.get_selected_rows()

        if len(rows) == 0:
            self.status_bar.push(
                    1, _('Selection cleared').format(len(rows)))

        elif len(rows) == 1:
            # If it is a file
            row_content = model[rows[0]][0]

            if rows[0].get_depth() == 2:
                self.status_bar.push(1,
                        _("'{}'; modified on {}").format(
                            os_functions.get_pretty_name(row_content),
                            datetime.fromtimestamp(
                                os.path.getmtime(row_content)).strftime(
                                    '%Y-%m-%d, %H:%M:%S')))
            else:
                self.status_bar.push(1,
                    _("{} ({} files)").format(
                        row_content,
                        model.iter_n_children(
                            model.get_iter(rows[0]))))

        else:
            # Do not allow parent rows in multiple row selection
            for row in rows:
                if row.get_depth() == 1:
                    hash_tree_selection.unselect_path(row)

                self.status_bar.push(
                        1, _('{} rows selected').format(
                            hash_tree_selection.count_selected_rows()))

    def on_row_inserted(self, model, path, iter_):
        if settings.expand_one_row_at_once:
            self.hash_tree_view.collapse_all()
        if settings.expand_rows_as_inserted:
            self.hash_tree_view.expand_to_path(path)
        if settings.scroll_to_inserted_rows:
            self.hash_tree_view.scroll_to_cell(
                    path, None, False, 0.0, 0.0)

    def on_row_activated(self, tree_view, path, column):
        depth = path.get_depth()

        # Parent (code)
        if depth == 1:
            if settings.expand_one_row_at_once:
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
            self.cancellable.cancel()

    def handle_signal(self, signal_name, *args):
        if self.task is not None and self.task.get_completed():
            return

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
            total_iterations, total_files, elapsed_time = args

            message = _(
                    '{} repetitions found before cancelling; {} files processed; elapsed: {}').format(
                            total_iterations, total_files, elapsed_time)

            self.status_bar.remove_all(1)
            self.status_bar.push(1, message)

        elif signal_name == 'limit-reached':
            total_iterations, total_files, elapsed_time = args

            message = _(
                    '{} repetitions found before reaching limit of {} files; elapsed: {}').format(
                            total_iterations, total_files, elapsed_time)

            self.status_bar.remove_all(1)
            self.status_bar.push(1, message)

        elif signal_name == 'finished':
            total_iterations, total_files, elapsed_time = args

            message = _('{} repetitions found within {} files; elapsed: {}').format(
                    total_iterations, total_files, elapsed_time)

            self.status_bar.remove_all(1)
            self.status_bar.push(1, message)

        elif signal_name == 'insufficient-permissions':
            item_dirname, item_basename = args

            message = _('Not enough permissions to open \'{}\'').format(
                    os.path.join(item_dirname, item_basename))
            self.status_bar.push(1, message)

        # Cancel the idle_add call
        return False

