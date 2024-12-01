from utils import hashing, os_functions
from utils.dict_to_class import DictToClass
from collections import deque, defaultdict

class AppStatus:
    # In a C application, this would be accessed with a mutex
    cancelling = False

def blocking(settings_dict, signal_handler):
    # Avoid dictionary lookups
    settings = DictToClass(settings_dict)

    signal_handler.emit('started')

    # Use defaultdict instead of a normal dictionary
    hash_dict = defaultdict(list)

    total_iterations = 0
    total_files = 0

    directory_queue = deque([settings.path])

    while directory_queue:
        if AppStatus.cancelling:
            signal_handler.emit('cancelled', total_iterations, total_files)
            return

        item_dirname = directory_queue.popleft()

        try:
            # List the directory contents
            dir_listing = os_functions.list_dir(item_dirname)
        except PermissionError:
            signal_handler.emit('insufficient-permissions', item_dirname, '')
            continue

        for item_basename in dir_listing:
            # Check for cancellation during iteration
            if AppStatus.cancelling:
                signal_handler.emit('cancelled', total_iterations, total_files)
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

                if not os_functions.dir_perms_OK(item_path):
                    signal_handler.emit('insufficient-permissions', item_dirname, item_basename)
                    continue

                # Essential
                directory_queue.append(item_path)

            # Check if the item is a file
            elif os_functions.is_file(item_path):
                if not settings.read_dotted_files and item_basename.startswith('.'):
                    continue

                # Check file permissions
                if not os_functions.file_perms_R_OK(item_path):
                    signal_handler.emit('insufficient-permissions', item_dirname, item_basename)
                    continue

                # Hashing based on the selected method
                if settings.method == 0:
                    code = hashing.sha1(item_path)
                elif settings.method == 1:
                    code = hashing.adler32(item_path)
                elif settings.method == 2:
                    code = hashing.size(item_path)
                elif settings.method == 3:
                    code = item_basename
                else:
                    # Unrecognized method (unlikely)
                    continue

                # Append the item path to the hash_dict
                hash_dict[code].append(item_path)
                len_group = len(hash_dict[code])

                # A parent can only be added along with two files
                if len_group == 2:
                    total_iterations += 1
                    signal_handler.emit(
                        'append-parent',
                        code,
                        hash_dict[code][0],
                        hash_dict[code][1]
                    )
                elif len_group > 2:
                    signal_handler.emit('append-child', code, item_path)

                total_files += 1

                # Check if the file limit has been reached
                if settings.limit != 0 and total_files >= settings.limit:
                    signal_handler.emit(
                            'limit-reached', total_iterations, total_files)
                    return

    signal_handler.emit('finished', total_iterations, total_files)
