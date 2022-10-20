'''
Home to MiscCommand and friends for cAppInstaller
'''

import getpass
import queue
import pathlib
import tempfile

from .util import subprocess_call_live_output
from .strings import ADD_ADMIN_CMD_PROMPT_VIA_SHIFT_RIGHT_CLICK_REG

CHECKBOXES_PER_ROW = 2

class MiscCommand:
    '''
    A generic command to run as an action
    '''
    def __init__(self, cmd):
        ''' cmd is a shell command to run '''
        self.cmd = cmd

    def install(self, output_queue: queue.Queue) -> int:
        '''
        This is the function called by the GUI to install/run.
        '''
        return subprocess_call_live_output(output_queue, self.cmd)

class RegistryInstallCommand(MiscCommand):
    '''
    A command to run a .reg file
    '''
    def __init__(self, reg_file_text: str):
        '''
        The reg_file_text is saved to a temp .reg file then ran during install()
        '''
        self.reg_file_text = reg_file_text

        temp_file = tempfile.NamedTemporaryFile().name + '.reg'
        pathlib.Path(temp_file).write_text(self.reg_file_text)
        MiscCommand.__init__(self, 'reg import "%s"' % temp_file)

class SymlinkPython3ToPython3X(MiscCommand):
    '''
    A command to Symlink Python3 to Python3X'''
    def __init__(self):
        self.python_path = pathlib.Path('C:/Python3')

    def get_latest_python_folder(self):
        '''
        Gets the latest version of Python 3 in C:/
        '''
        return pathlib.Path('C:/Python' + str(sorted(int(str(s).split('Python')[-1]) for s in list(pathlib.Path('C:/').glob("Python3*")))[-1]))

    def install(self, output_queue: queue.Queue) -> int:
        '''
        This is the function called by the GUI to symlink
        C:/Python3 to C:/Python3X
        '''
        if self.python_path.is_symlink():
            self.python_path.unlink()

        latest_py = self.get_latest_python_folder()
        output_queue.put_nowait([f'Symlinking: {self.python_path} -> {latest_py}'])
        self.python_path.symlink_to(latest_py)
        return 0

# todo:
# Add C:/Python/bin to PATH
MISC_COMMANDS = {
    f'Add Admin Cmd Prompt via Shift/Right Click' : RegistryInstallCommand(ADD_ADMIN_CMD_PROMPT_VIA_SHIFT_RIGHT_CLICK_REG),
    f'Symlink Python3 -> Python3X' : SymlinkPython3ToPython3X(),
    f'Add C:/Python3 to System PATH' : MiscCommand(f'setx /m PATH "C:\Python3;C:\Python3\Scripts;%PATH%"'),
    f'Chown C:/Python3 for {getpass.getuser()}' : MiscCommand(f'icacls C:/Python3 /t /q /grant "{getpass.getuser()}":(OI)(CI)F'),
}