'''
Home to MiscCommand and friends for cAppInstaller
'''

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

    def install(self, output_queue: queue.Queue):
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


# todo:
# Symlink C:/Python to C:/Python3X
# Add C:/Python/bin to PATH
# Enable Windows Sandbox: powershell Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -All -Online
MISC_COMMANDS = {
    'Add Admin Cmd Prompt via Shift/Right Click' : RegistryInstallCommand(ADD_ADMIN_CMD_PROMPT_VIA_SHIFT_RIGHT_CLICK_REG)
}