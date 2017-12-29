import os
import sys

# make sure we can get to ctk
THIS_FOLDER = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(THIS_FOLDER, 'cTk', 'ctk'))
from ctk import *

APPS = {
    # Pretty: Actual
    '7-Zip' : '7zip',
    'Classic Shell' : 'classic-shell -installArgs ADDLOCAL=ClassicStartMenu',
    'CPU-Z' : 'cpu-z',
    'Filezilla' : 'filezilla',
    'Git' : 'git',
    'Git Extensions': 'gitextensions',
    'Google Chrome': 'googlechrome',
    'GrepWin': 'grepwin',
    'HxD': 'hxd',
    'Notepad Plus Plus': 'notepadplusplus',
    'Path Copy Copy': 'path-copy-copy',
    'Process Explorer': 'procexp',
    'Pip': 'pip',
    'VNC Viewer': 'vnc-viewer',
    'Skype': 'skype',
    'Steam': 'steam',
    'Sudo': 'sudo',
    'TortoiseHg': 'tortoisehg',
    'Visual Studio Code': 'visualstudiocode',
    'Visual Studio 2017 Community': 'visualstudio2017community visualstudio2017-workload-nativecrossplat visualstudio2017-workload-nativedesktop visualstudio2017-workload-universal windows-sdk-10.1',
    'VLC': 'vlc',
    'WinDirStat': 'windirstat',
    'WinMerge': 'winmerge',
}

def prettyNameToCheckboxName(prettyName):
    return '_' + prettyName.replace(' ', '_SPACE_')

def checkboxNameToPrettyName(checkboxName):
    return checkboxName[1:].replace('_SPACE_', ' ')

class Gui(CtkWindow):
    def __init__(self):
        CtkWindow.__init__(self)
        self.title("cAppInstaller")

        rowNum = 0
        for prettyName in sorted(APPS.keys()):
            packageNameAndArgs = APPS[prettyName]
            v = tk.IntVar()
            self.addWidget(tk.Checkbutton, text=prettyName, name=prettyNameToCheckboxName(prettyName), y=rowNum, variable=v, 
                gridKwargs={
                    'sticky':tk.W
                }
            )
            getattr(self, prettyNameToCheckboxName(prettyName)).checked = v
            rowNum += 1

        self.addWidget(CtkFrame, name='frameButtons', y=rowNum)
        self.frameButtons.addWidget(tk.Button, text="Install Selected", name='buttonInstall', command=self.installSelected, y=rowNum, x=1)
        self.frameButtons.addWidget(tk.Button, text="Select All", name='buttonSelectAll', command=self.selectAll, y=rowNum, x=0)
        self.mainloop()

    def selectAll(self):
        for i in self._getAllCheckboxes():
            i.select()

    def _getAllCheckboxes(self):
        checkboxes = []
        for thing in dir(self):
            thingAsObj = getattr(self, thing)
            if isinstance(thingAsObj, tk.Checkbutton):   
                checkboxes.append(thingAsObj)

        return checkboxes

    def _getInstallCommandList(self):
        retList = []
        for checkbox in self._getAllCheckboxes():
            if checkbox.checked.get():
                cmd = 'choco install %s' % APPS[checkbox.cget('text')]
                retList.append(cmd)

        return retList

    def installSelected(self):
        installCommands = self._getInstallCommandList()
        with self.busyCursor():
            for i in installCommands:
                print ("About to execute: %s" % i)
                os.system(i)

            print ("Done")

if __name__ == '__main__':
    g = Gui()