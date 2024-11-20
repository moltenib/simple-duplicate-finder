import locale

language = locale.getlocale()[0]

if language is None:
    language = ''

if language.startswith('es'):
    # Spanish
    AVAILABLE_METHODS = ('SHA-1', 'Adler-32', 'Tamaño', 'Nombre')
    CHOOSE_PATH = 'Elegir ruta'
    START = 'Iniciar'
    STOP = 'Detener'
    CANCEL = 'Cancelar'
    CONTINUE = 'Continuar'

    WELCOME = 'Para empezar, elija un directorio en la barra de arriba'
    STARTED = 'Trabajando...'
    INSUFFICIENT_PERMISSIONS = 'Permisos insuficientes para leer \'{}\' '
    LIMIT_REACHED = \
        '{} repeticiones encontradas antes de alcanzar límite;' + \
        ' {} archivos analizados'
    CANCELLED = '{} repeticiones encontradas antes de cancelar;' + \
        ' {} archivos analizados'
    FINISHED = '{} repeticiones encontradas en {} archivos'
    FILE_OPENED = '\'{}\' abierto'
    FILE_NOT_OPENED = 'No puede abrir \'{}\''
    FILE_SELECTED = '\'{}\', archivo {}, {} {}' # Name, type, size, size unit
    ROUTINE_FAILED = 'Error: rutina \'{}\' ha fallado'

    CONFIRM_DELETION_ONE = '¿Está seguro de borrar el siguiente archivo?\n\n{}'
    CONFIRM_DELETION_MANY = '¿Está seguro de borrar los siguientes archivos?\n\n{}'
    FILES_DELETED = 'Se han borrado archivos'

    SETTINGS = 'Configuraciones'
    ABOUT = 'Acerca de'
    LOAD_DEFAULT_SETTINGS = 'Cargar predeterminados'

    ASK_BEFORE_DELETING = 'Preguntar antes de borrar'
    BEHAVIOUR = 'Comportamiento'
    INTERFACE = 'Interfaz'

    ASK_BEFORE_DELETING_ONE = 'Un archivo'
    ASK_BEFORE_DELETING_MANY = 'Múltiples archivos'

    EXPAND_ROWS_AS_INSERTED = 'Expandir filas mientras aparecen'
    EXPAND_ONE_ROW_AT_ONCE = 'Expandir una fila a la vez'
    SCROLL_TO_INSERTED_ROWS = 'Navegar a las filas insertadas'
    SEND_NOTIFICATIONS = 'Enviar notificationes'
    CLEAR_TREE = 'Borrar lista de archivos antes de empezar de nuevo'

    FOLLOW_LINKS = 'Seguir enlaces simbólicos'
    READ_DOTTED_FILES = 'Leer archivos escondidos'
    READ_DOTTED_DIRECTORIES = 'Leer directorios escondidos'
    FILE_LIMIT = 'Parar luego de alcanzar un límite de archivos'

    FONT_DEFAULT = 'Fuente de facto'
else:
    # English
    AVAILABLE_METHODS = ('SHA-1', 'Adler-32', 'File size', 'File name')
    CHOOSE_PATH = 'Choose path'
    START = 'Start'
    STOP = 'Stop'
    CANCEL = 'Cancel'
    CONTINUE = 'Continue'

    WELCOME = 'To begin, please choose a directory from the top bar'
    STARTED = 'Working...'
    INSUFFICIENT_PERMISSIONS = 'Not enough permissions to read \'{}\' '
    LIMIT_REACHED = \
        '{} repetitions found before reaching limit of {} files'
    CANCELLED = '{} repetitions found before cancelling; {} files processed'
    FINISHED = '{} repetitions found within {} files'
    FILE_OPENED = '\'{}\' opened'
    FILE_NOT_OPENED = 'Unable to open \'{}\''
    FILE_SELECTED = '\'{}\', {} file, {} {}' # Name, type, size, size unit
    ROUTINE_FAILED = 'Error: routine \'{}\' has failed'

    CONFIRM_DELETION_ONE = 'Are you sure you want to delete the following file?\n\n{}'
    CONFIRM_DELETION_MANY = 'Are you sure you want to delete the following files?\n\n{}'
    FILES_DELETED = 'Files have been deleted'

    SETTINGS = 'Settings'
    ABOUT = 'About'
    LOAD_DEFAULT_SETTINGS = 'Load defaults'

    ASK_BEFORE_DELETING = 'Ask before deleting'
    BEHAVIOUR = 'Behaviour'
    INTERFACE = 'Interface'

    ASK_BEFORE_DELETING_ONE = 'One file'
    ASK_BEFORE_DELETING_MANY = 'Multiple files'

    EXPAND_ROWS_AS_INSERTED = 'Expand rows as they appear'
    EXPAND_ONE_ROW_AT_ONCE = 'Expand one row at once'
    SCROLL_TO_INSERTED_ROWS = 'Scroll to inserted rows'
    SEND_NOTIFICATIONS = 'Send notifications'
    CLEAR_TREE = 'Clear the file list before starting over'

    FOLLOW_LINKS = 'Follow symbolic links'
    READ_DOTTED_FILES = 'Read dotted files'
    READ_DOTTED_DIRECTORIES = 'Read dotted directories'
    FILE_LIMIT = 'Stop after a file limit is reached'

    FONT_DEFAULT = 'Default font'
