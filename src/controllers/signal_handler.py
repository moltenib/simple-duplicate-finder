from gi.repository import GObject

class SignalHandler(GObject.GObject):
    def __init__(self):
        GObject.GObject.__init__(self)

        GObject.signal_new(
                'started', self,
                GObject.SIGNAL_RUN_CLEANUP, None,
                ())
        GObject.signal_new(
                'append-parent', self,
                GObject.SIGNAL_RUN_CLEANUP, None,
                # Hash, file 1, file 2
                (str, str, str,))
        GObject.signal_new(
                'append-child', self,
                GObject.SIGNAL_RUN_CLEANUP, None,
                # Hash, file
                (str, str,))
#        GObject.signal_new(
#                'ignored-link', self,
#                GObject.SIGNAL_RUN_CLEANUP, None,
#                # Dirname, basename
#                (str, str,))
#        GObject.signal_new(
#                'ignored-dotted-dir', self,
#                GObject.SIGNAL_RUN_CLEANUP, None,
#                # Dirname, basename
#                (str, str,))
        GObject.signal_new(
                'insufficient-permissions', self,
                GObject.SIGNAL_RUN_CLEANUP, None,
                # Dirname, basename
                (str, str,))
#        GObject.signal_new(
#                'ignored-dotted-file', self,
#                GObject.SIGNAL_RUN_CLEANUP, None,
#                # Basename, dirname
#                (str, str,))
        GObject.signal_new(
                'limit-reached', self,
                GObject.SIGNAL_RUN_LAST, None,
                # Total found, total files
                (int, int,))
        GObject.signal_new(
                'finished', self,
                GObject.SIGNAL_RUN_LAST, None,
                # Total found, total files
                (int, int,))
        GObject.signal_new(
                'cancelled', self,
                GObject.SIGNAL_RUN_LAST, None,
                (int, int,))

