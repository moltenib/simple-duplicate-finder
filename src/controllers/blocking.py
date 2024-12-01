from utils import hashing, os_functions
from utils.dict_to_class import DictToClass

from collections import deque

class AppStatus:
    cancelling = False

def messy_code_block(settings_dict, signal_handler):
    # Avoid dictionary lookups
    settings = DictToClass(settings_dict)

    hash_dict = {}
    total_iterations = 0
    total_files = 0

    signal_handler.emit('started')

    directory_queue = deque([settings.path])

    while directory_queue:
        # Descend into new directory
        item_dirname = directory_queue.popleft()

        try:
            dir_listing = os_functions.list_dir(item_dirname)
        except PermissionError:
            signal_handler.emit('insufficient-permissions', item_dirname, '')
            continue

        for item_basename in dir_listing:
            if AppStatus.cancelling:
                signal_handler.emit('cancelled', total_iterations, total_files)
                return

            item_path = os_functions.path_join(item_dirname, item_basename)

            if (not settings.follow_symbolic_links and os_functions.is_link(item_path)):
                continue

            if os_functions.is_dir(item_path):
                if (not settings.read_dotted_directories and item_basename.startswith('.')):
                    continue
                if not os_functions.dir_perms_OK(item_path):
                    signal_handler.emit('insufficient-permissions', item_dirname, item_basename)
                    continue

                # Essential
                directory_queue.append(item_path)

            elif os_functions.is_file(item_path):
                if (not settings.read_dotted_files and item_basename.startswith('.')):
                    continue
                if not os_functions.file_perms_R_OK(item_path):
                    signal_handler.emit('insufficient-permissions', item_dirname, item_basename)
                    continue

                # Hashing based on the selected method
                if settings.method == 0:
                    code_ = hashing.sha1(item_path)
                elif settings.method == 1:
                    code_ = hashing.adler32(item_path)
                elif settings.method == 2:
                    code_ = hashing.size(item_path)
                elif settings.method == 3:
                    code_ = item_basename

                if code_ in hash_dict:
                    hash_dict[code_].append(item_path)
                    len_ = len(hash_dict[code_])
                    if len_ > 1:
                        if len_ == 2:
                            total_iterations += 1
                            signal_handler.emit(
                                'append-parent',
                                code_,
                                str(hash_dict[code_][0]),
                                str(hash_dict[code_][1])
                            )
                        else:
                            signal_handler.emit('append-child', code_, item_path)
                else:
                    hash_dict[code_] = [item_path]

                total_files += 1
                if settings.limit != 0 and total_files >= settings.limit:
                    signal_handler.emit('limit-reached', total_iterations, total_files)
                    return

    signal_handler.emit('finished', total_iterations, total_files)

