import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from utils.settings import settings

class TreeModel(Gtk.TreeStore):
    def __init__(self):
        Gtk.TreeStore.__init__(self, str)
        self.hash_to_iter = {}

    def add_parent(self, hash_):
        if not self.hash_to_iter.__contains__(hash_):
            iter_ = self.append(None, [hash_])
            self.hash_to_iter[hash_] = iter_

    def add_child(self, hash_, file_):
        self.insert_after(
                self.hash_to_iter[hash_],
                None,
                [file_])

    def clear_all(self):
        self.clear()
        self.hash_to_iter.clear()

    def print_to_file(self, file_name):
        with open(file_name, 'w') as f:
            # This assumes the first row is a parent
            parent_iter = self.get_iter_first()

            while parent_iter:
                current_hash = self[parent_iter][0]

                # Iterate through its children
                child_iter = self.iter_children(parent_iter)

                while child_iter:
                    current_file = self[child_iter][0]

                    # Using tab as a separator
                    f.write('{}\t{}\n'.format(current_hash, current_file))

                    child_iter = self.iter_next(child_iter)

                parent_iter = self.iter_next(parent_iter)


class TreeView(Gtk.TreeView):
    def __init__(self, model):
        Gtk.TreeView.__init__(self)
        renderer = Gtk.CellRendererText(
                font=settings.font)
        hash_tree_column = Gtk.TreeViewColumn(
            'Codes', renderer, text=0)
        self.append_column(hash_tree_column)
        self.set_headers_visible(False)
        self.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.set_model(model)

