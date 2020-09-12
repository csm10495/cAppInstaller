'''
gui.py is a simple gui with options to install selected apps via choco in the background

~Charles Machalow via the MIT License
'''
import ctypes
import os
import subprocess
import sys
import time

APPS = {
    # Pretty: Actual
    '7-Zip' : '7zip',
    '8GadgetPack' : '8gadgetpack',
    'Adobe Reader' : 'adobereader',
    'API Monitor' : 'apimonitor',
    'Audacity' : 'audacity',
    'Authy' : 'authy-desktop',
    'BGInfo' : 'bginfo',
    'Classic Shell' : 'classic-shell -installArgs ADDLOCAL=ClassicStartMenu',
    'CPU-Z' : 'cpu-z',
    'CrystalDiskInfo' : 'crystaldiskinfo',
    'CrystalDiskMark' : 'crystaldiskmark',
    'DebugView' : 'dbgview',
    'Discord' : 'discord',
    'Epic Games Launcher' : 'epicgameslauncher',
    'Filezilla' : 'filezilla',
    'Git' : 'git',
    'Git Extensions': 'gitextensions',
    'Google Chrome': 'googlechrome',
    'GrepWin': 'grepwin',
    'HxD': 'hxd',
    'KiTTY' : 'kitty',
    'Logitech Gaming' : 'logitechgaming',
    'Minecraft': 'minecraft',
    'Mp3tag' : 'mp3tag',
    'Notepad Plus Plus': 'notepadplusplus',
    'Path Copy Copy': 'path-copy-copy',
    'Process Explorer': 'procexp',
    'PuTTY' : 'putty',
    'Python 2': 'python2 /InstallDir "C:\Python27"',
    'Python 3': 'python --version 3.7.0 --params "/InstallDir:"C:\Python37"',
    'VNC Viewer': 'vnc-viewer',
    'Skype': 'skype --version 7.41.0.10101',
    'Steam': 'steam',
    'Sudo': 'sudo',
    'Teracopy': 'teracopy',
    'TortoiseHg': 'tortoisehg',
    'Transmission': 'transmission',
    'VirtualBox' : 'virtualbox',
    'Visual Leak Detector' : 'visualleakdetector',
    'Visual Studio Code': 'visualstudiocode',
    'Visual Studio 2017 Community': 'visualstudio2017community visualstudio2017-workload-nativecrossplat visualstudio2017-workload-nativedesktop visualstudio2017-workload-universal windows-sdk-10.1',
    'VLC': 'vlc',
    'Wget' : 'wget',
    'WinDirStat': 'windirstat',
    'WinMerge': 'winmerge',
    'Xming' : 'xming',
}

MAX_APP_PER_COLUMN = 15

def ensureHasChoco():
    '''
    by time this function ends, the system should have choco
    '''
    try:
        subprocess.check_output('where choco', stderr=subprocess.STDOUT, shell=True).strip()
        print ("choco detected")
    except Exception as ex:
        print ("Installing choco")
        os.system(r'''@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"''')

def getChoco():
    '''
    returns the location of the choco executable
    '''
    choco = r"C:\ProgramData\chocolatey\choco.exe"
    if not os.path.isfile(choco):
        raise EnvironmentError("Cannot find choco!")
    return choco

def getGit():
    '''
    returns the location of the git executable
    '''
    try:
        return '\"%s\"' % subprocess.check_output('where git', stderr=subprocess.STDOUT, shell=True).strip().decode()
    except:
        return os.path.expandvars('\"%PROGRAMFILES%/Git/cmd/git.exe\"')

def getProxy():
    '''
    returns the proxy if Windows is using one. Otherwise returns None.
    '''
    try:
        proxy = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings")
        server, t = winreg.QueryValueEx(proxy, "ProxyServer")
        enabled, t = winreg.QueryValueEx(proxy, "ProxyEnable")
        if enabled:
            return server
    except WindowsError:
        print ('-I- Could not find any proxy settings')
    return None

if __name__ == '__main__':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Please Re-run as admin")
        os.system('pause')
        raise EnvironmentError("Please run as admin")

    # make sure we can get to ctk
    THIS_FOLDER = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(THIS_FOLDER, 'cTk', 'ctk'))
    try:
        from ctk import tk, CtkWindow, CtkFrame
        from widgets import ScrollableText
    except ImportError:
        if '-n' not in sys.argv:
            print ("Had trouble finding ctk... will try to download it.")
            try:
                import _winreg as winreg # py2
            except ImportError:
                import winreg # py3

            ensureHasChoco()
            # try to download ctk 
            os.system(getChoco() + " install git -y")
            proxy = getProxy()

            if proxy:
                cmd = '%s -c http.proxy=%s clone https://github.com/csm10495/cTk.git "%s/cTk"' % (getGit(), proxy, THIS_FOLDER)
            else:
                cmd = '%s clone https://github.com/csm10495/cTk.git "%s/cTk"' % (getGit(), THIS_FOLDER)

            print (subprocess.check_output(cmd, shell=True))
            print ("Re-running me!")
            sys.exit(os.system('%s %s -n' % (sys.executable, __file__)))
        else:
            print ("Not going to try to rerun self again!")
            raise 

    class AppToInstallWidget(CtkFrame):
        '''
        each one of these is an app to install and a text for status
        '''
        def __init__(self, *args, **kwargs):
            '''
            initializer. kwargs has a prettyAppName for the name of the app to install
            '''
            self.prettyAppName = kwargs['prettyAppName']
            del kwargs['prettyAppName']
            CtkFrame.__init__(self, *args, **kwargs)
            self.checkState = tk.IntVar()
            self.addWidget(tk.Checkbutton, name='check', text=self.prettyAppName, variable=self.checkState, y=0, x=0,
                    gridKwargs={
                        'sticky':tk.W
                    }
            ) 

            self.statusText = tk.StringVar()
            self.addWidget(tk.Label, name="label", textvariable=self.statusText, y=0, x=1,
                    gridKwargs={
                        'sticky':tk.E
                    }
            ) 

        def isChecked(self):
            '''
            returns True if the checkbox is checked
            '''
            return self.checkState.get()

        def select(self):
            '''
            selects the checkbox
            '''
            self.check.select()

        def deselect(self):
            '''
            deselects the checkbox
            '''
            self.check.deselect()

        def getPrettyAppName(self):
            '''
            gets this app's pretty name
            '''
            return self.prettyAppName

        def getStatusText(self):
            '''
            get the current status text
            '''
            return self.statusText.get()

        def setStatusText(self, txt, color):
            '''
            sets the current status text and color
            '''
            self.statusText.set(txt)
            self.label.configure(fg=color)
            self.update()

    class Gui(CtkWindow):
        '''
        gui that displays all apps that we have the option of installing.
        '''
        def __init__(self):
            CtkWindow.__init__(self)
            self.title("cAppInstaller")

            rowNum = 0
            colNum = 0
            self._appWidgets = []
            for idx, prettyName in enumerate(sorted(APPS.keys())):
                if idx % MAX_APP_PER_COLUMN == 0 and idx != 0:
                    colNum += 1

                self.addWidget(AppToInstallWidget, name='tmp', y=rowNum % MAX_APP_PER_COLUMN, x=colNum, prettyAppName=prettyName,
                    gridKwargs={
                        'sticky':tk.W
                    }
                )
                self._appWidgets += [self.tmp]

                rowNum += 1

            colNum += 1

            self.addWidget(CtkFrame, name='frameButtons', y=rowNum)
            self.frameButtons.addWidget(tk.Button, text="Install Selected", name='buttonInstall', command=self.installSelected, y=rowNum, x=1)
            self.frameButtons.addWidget(tk.Button, text="Select All", name='buttonSelectAll', command=self.selectAll, y=rowNum, x=0)
            self.addWidget(ScrollableText, name='console', x=colNum, gridKwargs={"rowspan": 100, "sticky" : tk.NSEW})

            self.expandRow(rowNum)
            self.expandColumn(colNum)
            self.mainloop()

        def selectAll(self):
            '''
            selects all checkboxes
            '''
            for i in self._appWidgets:
                i.select()

        def installSelected(self):
            '''
            installs all selected 
            '''
            with self.busyCursor():
                for checkbox in self._appWidgets:
                    if checkbox.isChecked():
                        cmd = '%s install %s -y --ignorepackagecodes' % (getChoco(), APPS[checkbox.getPrettyAppName()])
                        
                        self.console.appendText("-I- About to execute: %s \n" % cmd)
                        checkbox.setStatusText("In Progress", 'blue')
                        
                        if self.systemCall(cmd) == 0:
                            checkbox.setStatusText("Success", 'green')
                            checkbox.deselect() # deselect
                        else:
                            checkbox.setStatusText("Failure", 'red')
                        
                        self.update()

                self.console.appendText('=' * 45 + "\n")
                self.console.appendText("-I - Done \n ")
                self.console.appendText('=' * 45 + "\n")

        def systemCall(self, cmd):
            '''
            makes a system call
            '''
            return subprocess.call(cmd, shell=True)

    ensureHasChoco()
    g = Gui()
