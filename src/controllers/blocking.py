from collections import deque, defaultdict
from gi.repository import GLib
from utils import hashing, os_functions
from utils.elapsed_time import elapsed_time

from datetime import datetime

def blocking(task, settings, callback):
    GLib.idle_add(callback, 'started')

    # Use defaultdict instead of a normal dictionary
    hash_dict = defaultdict(list)

    total_iterations = 0
    total_files = 0

    time_started = datetime.now()

    # Use a queue for breadth-first search
    directory_queue = deque([settings.path])

    # Use GObject threading techniques
    cancellable = task.get_cancellable()

    while directory_queue:
        if cancellable.is_cancelled():
            GLib.idle_add(
                    callback,
                    'cancelled',
                    total_iterations,
                    total_files,
                    elapsed_time(time_started))
            return

        item_dirname = directory_queue.popleft()

        try:
            # List the directory contents
            dir_listing = os_functions.list_dir(item_dirname)

        except:
            # Ignore all errors
            continue

        for item_basename in dir_listing:
            # Check for cancellation during iteration
            if cancellable.is_cancelled():
                GLib.idle_add(
                        callback,
                        'cancelled',
                        total_iterations,
                        total_files,
                        elapsed_time(time_started))
                return

            # Construct the full path once
            item_path = os_functions.path_join(
                    item_dirname, item_basename)

            # Skip symbolic links if not following them
            if not settings.follow_symbolic_links and os_functions.is_link(item_path):
                continue

            # Check if the item is a directory
            if os_functions.is_dir(item_path):
                if not settings.read_dotted_directories and item_basename.startswith('.'):
                    continue

                # Essential
                directory_queue.append(item_path)

            # Check if the item is a file
            elif os_functions.is_file(item_path):
                if not settings.read_dotted_files and item_basename.startswith('.'):
                    continue

                # Check file permissions
                # os.access() does not work on NT
                try:
                   # Hashing based on the selected method
                   if settings.method == 0:
                       code = hashing.sha1(item_path)
                   elif settings.method == 1:
                       code = hashing.adler32(item_path)
                   elif settings.method == 2:
                       code = hashing.modification_time(item_path)
                   elif settings.method == 3:
                       code = item_basename

                except:
                    # Ignore all errors
                    continue

                # Only look up the item once
                current_hash_dict_item = hash_dict[code]

                # Append it to the current hash_dict item
                current_hash_dict_item.append(item_path)

                # A parent can only be added along with two files
                if len(current_hash_dict_item) == 2:
                    total_iterations += 1
                    GLib.idle_add(
                        callback,
                        'append-parent',
                        code,
                        current_hash_dict_item[0],
                        current_hash_dict_item[1])

                elif len(current_hash_dict_item) > 2:
                    GLib.idle_add(
                            callback, 'append-child', code, item_path)

                total_files += 1

                # Check if the file limit has been reached
                if settings.limit != 0 and total_files >= settings.limit:
                    GLib.idle_add(
                            callback,
                            'limit-reached',
                            total_iterations,
                            total_files,
                            elapsed_time(time_started))
                    return

    GLib.idle_add(
            callback,
            'finished',
            total_iterations,
            total_files,
            elapsed_time(time_started))
