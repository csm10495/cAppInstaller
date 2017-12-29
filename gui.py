import ctypes
import os
import subprocess
import sys

# make sure we can get to ctk
THIS_FOLDER = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(THIS_FOLDER, 'cTk', 'ctk'))
from ctk import *

APPS = {
    # Pretty: Actual
    '7-Zip' : '7zip',
    'Audacity' : 'audacity',
    'Classic Shell' : 'classic-shell -installArgs ADDLOCAL=ClassicStartMenu',
    'CPU-Z' : 'cpu-z',
    'CrystalDiskInfo' : 'crystaldiskinfo',
    'CrystalDiskMark' : 'crystaldiskmark',
    'DebugView' : 'dbgview',
    'Filezilla' : 'filezilla',
    'Git' : 'git',
    'Git Extensions': 'gitextensions',
    'Google Chrome': 'googlechrome',
    'GrepWin': 'grepwin',
    'HxD': 'hxd',
    'Mp3tag' : 'mp3tag',
    'Notepad Plus Plus': 'notepadplusplus',
    'Path Copy Copy': 'path-copy-copy',
    'Process Explorer': 'procexp',
    'Python 2': 'python2 /InstallDir "C:\Python27"',
    'VNC Viewer': 'vnc-viewer',
    'Skype': 'skype',
    'Steam': 'steam',
    'Sudo': 'sudo',
    'TortoiseHg': 'tortoisehg',
    'VirtualBox' : 'virtualbox',
    'Visual Leak Detector' : 'visualleakdetector',
    'Visual Studio Code': 'visualstudiocode',
    'Visual Studio 2017 Community': 'visualstudio2017community visualstudio2017-workload-nativecrossplat visualstudio2017-workload-nativedesktop visualstudio2017-workload-universal windows-sdk-10.1',
    'VLC': 'vlc',
    'Wget' : 'wget',
    'WinDirStat': 'windirstat',
    'WinMerge': 'winmerge',
}

def prettyNameToCheckboxName(prettyName):
    return '_' + prettyName.replace(' ', '_SPACE_')

def ensureHasChoco():
    '''
    by time this function ends, the system should have choco
    '''
    try:
        subprocess.check_output('where choco', stderr=subprocess.STDOUT, shell=True)
        print ("choco detected")
    except Exception as ex:
        print ("Installing choco")
        os.system(r'''@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"''')

def getChoco():
    '''
    returns the location of the choco executable
    '''
    try:
        return subprocess.check_output('where choco', stderr=subprocess.STDOUT, shell=True).strip()
    except:
        return os.path.expandvars(r'%ALLUSERSPROFILE%\chocolatey\bin\choco')

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
                cmd = '%s install %s -y' % (getChoco(), APPS[checkbox.cget('text')])
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
    if not ctypes.windll.shell32.IsUserAnAdmin():
        raise EnvironmentError("Please run as admin")

    ensureHasChoco()
    g = Gui()