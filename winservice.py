# Usage : python winservice.py install then start, stop, remove.
import logging
import servicemanager
import win32service
import win32serviceutil
import win32event
import sys
import ctypes

from home_commands import Server

DEBUG = False
logging.basicConfig(
    filename="c:\\Temp\\home-commands.log",
    format="%(asctime)s:%(levelname)s %(module)s:%(lineno)d> %(message)s",
    level=logging.DEBUG if DEBUG else logging.INFO,
)


class LogWriter:
    def __init__(self, level=logging.INFO):
        self.level = level

    def write(self, data):
        logging.log(self.level, data)

    def flush(self):
        pass


def run_as_admin(argv=None, debug=False):
    shell32 = ctypes.windll.shell32
    if argv is None and shell32.IsUserAnAdmin():
        return True

    if argv is None:
        argv = sys.argv
    if hasattr(sys, "_MEIPASS"):
        # Support pyinstaller wrapped program.
        arguments = map(str, argv[1:])
    else:
        arguments = map(str, argv)
    argument_line = " ".join(arguments)
    executable = str(sys.executable)
    if debug:
        print("Command line: ", executable, argument_line)
    ret = shell32.ShellExecuteW(None, "runas", executable, argument_line, None, 1)
    if int(ret) <= 32:
        return False
    return None


class HomeCommandsService(win32serviceutil.ServiceFramework):
    _svc_name_ = "HomeCommands"
    _svc_display_name_ = "Home Commands"
    _svc_description_ = "Listen to commands from google home to control this computer."

    def __init__(self, args):
        logging.debug("Init.")
        self.server = Server()
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        logging.debug("Stop. %s", self.server)
        self.server.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        exit(0)

    def SvcDoRun(self):
        logging.debug("Do start.")
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        self.server.start()


if __name__ == "__main__":
    ret = run_as_admin(debug=DEBUG)
    if ret is True:
        try:
            if DEBUG:
                print("I have admin privilege.")
            win32serviceutil.HandleCommandLine(HomeCommandsService)
        finally:
            if DEBUG:
                input("Press ENTER to exit.")
    elif ret is None:
        print("Rerunning as admin in a separate window.")
    else:
        try:
            print("Error(ret=%d): cannot elevate privilege." % (ret,))
        finally:
            if DEBUG:
                input("Press ENTER to exit.")
else:
    sys.stdout = LogWriter()
    sys.stderr = LogWriter(level=logging.WARNING)
