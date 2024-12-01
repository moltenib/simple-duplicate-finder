from .strictly_gobject_related import GUISignalHandler

from gettext import gettext as _

class Enum:
    PARENT = 0
    CHILD = 1
    MESSAGE = 2
    CANCEL = 3
    LIMIT_REACHED = 4
    FINISH = 5

signal_handler = GUISignalHandler()
queue = []
handler_list = []

# Idle function
def run(window):
    if len(queue) > 0:
        i = queue.pop(0)
        if i[0] == Enum.PARENT:
            window.hash_tree_model.add_parent(i[1])
            window.hash_tree_model.add_child(i[1], i[2])
            window.hash_tree_model.add_child(i[1], i[3])
        elif i[0] == Enum.CHILD:
            window.hash_tree_model.add_child(i[1], i[2])
        elif i[0] == Enum.MESSAGE:
            window.status_bar.push(1, i[1])
        elif i[0] == Enum.CANCEL:
            message = _('{} repetitions found before cancelling; {} files processed').format(i[1], i[2])
            window.notify_os(message)
            window.status_bar.push(1, message)
            return False
        elif i[0] == Enum.LIMIT_REACHED:
            message = _('{} repetitions found before reaching limit of {} files').format(i[1], i[2])
            window.notify_os(message)
            window.status_bar.push(1, message)
            window.finish()
            return False
        elif i[0] == Enum.FINISH:
            message = _('{} repetitions found within {} files').format(i[1], i[2])
            window.notify_os(message)
            window.status_bar.push(1, message)
            window.finish()
            return False
    return True

def on_append_parent(signal_handler, hash_, file_1, file_2):
    queue.append((Enum.PARENT, hash_, file_1, file_2))

def on_append_child(signal_handler, hash_, file_):
    queue.append((Enum.CHILD, hash_, file_))

def on_started(signal_handler):
    queue.append((Enum.MESSAGE, _('Working...')))

def on_cancelled(signal_handler, total_iterations, total_files):
    queue.append((Enum.CANCEL, total_iterations, total_files))

def on_limit_reached(signal_handler, total_iterations, total_files):
    queue.append((Enum.LIMIT_REACHED, total_iterations, total_files))

def on_finished(signal_handler, total_iterations, total_files):
    queue.append((Enum.FINISH, total_iterations, total_files)) 

handler_list.append(
        signal_handler.connect_after(
            'append-parent', on_append_parent))
handler_list.append(
        signal_handler.connect_after(
            'append-child', on_append_child))
handler_list.append(
        signal_handler.connect_after(
            'started', on_started))
handler_list.append(
        signal_handler.connect_after(
            'cancelled', on_cancelled))
handler_list.append(
        signal_handler.connect_after(
            'limit-reached', on_limit_reached))
handler_list.append(
        signal_handler.connect_after(
            'finished', on_finished))

def destroy():
    for handler in handler_list:
        signal_handler.disconnect(handler)
