from utils import hashing, os_functions

class AppStatus:
    cancelling = False

def messy_code_block(settings, signal_handler):
    signal_handler.emit('started')
    old_dir = settings['path']
    hash_dict = {}
    total_iterations = 0
    total_files = 0
    directory_queue = [settings['path']]
    while len(directory_queue) > 0:
        item_dirname = directory_queue.pop(0)
        # Descend into new directory
        os_functions.chdir(item_dirname)
        for item_basename in os_functions.list_current_dir():
            if AppStatus.cancelling:
                os_functions.chdir(old_dir)
                signal_handler.emit(
                        'cancelled',
                        total_iterations,
                        total_files)
                return
            item = os_functions.abspath(item_basename)
            if (not settings['follow-symbolic-links']
                    and os_functions.is_link(item)):
#                signal_handler.emit(
#                        'ignored-link', item_dirname, item_basename)
                continue
            if os_functions.is_dir(item):
                if (not settings['read-dotted-directories']
                        and item_basename.startswith('.')):
#                    signal_handler.emit(
#                            'ignored-dotted-dir',
#                            item_dirname, item_basename)
                    continue
                if not os_functions.dir_perms_OK(item):
                    signal_handler.emit(
                            'insufficient-permissions',
                            item_dirname, item_basename)
                    continue
                # Essential
                directory_queue.append(item)
            elif os_functions.is_file(item):
                if (not settings['read-dotted-files']
                        and item_basename.startswith('.')):
#                    signal_handler.emit(
#                            'ignored-dotted-file',
#                            item_dirname, item_basename)
                    continue
                if not os_functions.file_perms_R_OK(item):
                    signal_handler.emit(
                            'insufficient-permissions',
                            item_dirname, item_basename)
                    continue
                if settings['method'] == 0:
                    code_ = hashing.sha1(item)
                elif settings['method'] == 1:
                    code_ = hashing.adler32(item)
                elif settings['method'] == 2:
                    code_ = hashing.size(item)
                elif settings['method'] == 3:
                    code_ = item_basename
                if hash_dict.__contains__(code_):
                    hash_dict[code_].append(item)
                    len_ = len(hash_dict[code_])
                    if len_ > 1:
                        if len_ == 2:
                            total_iterations += 1
                            signal_handler.emit(
                                    'append-parent',
                                    code_,
                                    str(hash_dict[code_][0]),
                                    str(hash_dict[code_][1]))
                        else:
                            signal_handler.emit(
                                    'append-child', code_, item)
                else:
                    hash_dict[code_] = [item]
                total_files += 1
                if settings['limit'] != 0:
                    if total_files >= settings['limit']:
                        os_functions.chdir(old_dir)
                        signal_handler.emit(
                                'limit-reached',
                                total_iterations,
                                total_files)
                        return
    os_functions.chdir(old_dir)
    signal_handler.emit(
            'finished',
            total_iterations,
            total_files)
