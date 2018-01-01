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
    'Transmission': 'transmission',
    'VirtualBox' : 'virtualbox',
    'Visual Leak Detector' : 'visualleakdetector',
    'Visual Studio Code': 'visualstudiocode',
    'Visual Studio 2017 Community': 'visualstudio2017community visualstudio2017-workload-nativecrossplat visualstudio2017-workload-nativedesktop visualstudio2017-workload-universal windows-sdk-10.1',
    'VLC': 'vlc',
    'Wget' : 'wget',
    'WinDirStat': 'windirstat',
    'WinMerge': 'winmerge',
}

def ensureHasChoco():
    '''
    by time this function ends, the system should have choco
    '''
    try:
        subprocess.check_output('where choco', stderr=subprocess.STDOUT, shell=True).strip().encode()
        print ("choco detected")
    except Exception as ex:
        print ("Installing choco")
        os.system(r'''@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"''')

def getChoco():
    '''
    returns the location of the choco executable
    '''
    try:
        return '\"%s\"' % subprocess.check_output('where choco', stderr=subprocess.STDOUT, shell=True).strip().encode()
    except:
        return os.path.expandvars('\"%ALLUSERSPROFILE%\chocolatey\bin\choco\"')

def getGit():
    '''
    returns the location of the git executable
    '''
    try:
        return '\"%s\"' % subprocess.check_output('where git', stderr=subprocess.STDOUT, shell=True).strip().encode()
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

def prettyNameToCheckboxName(prettyName):
    '''
    converts the pretty name to a variable name for the linked checkbox
    '''
    return '_' + prettyName.replace(' ', '_SPACE_')

if __name__ == '__main__':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        raise EnvironmentError("Please run as admin")

    # make sure we can get to ctk
    THIS_FOLDER = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(THIS_FOLDER, 'cTk', 'ctk'))
    try:
        from ctk import tk, CtkWindow, CtkFrame
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

    class Gui(CtkWindow):
        '''
        gui that displays all apps that we have the option of installing.
        '''
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
            '''
            selects all checkboxes
            '''
            for i in self._getAllCheckboxes():
                i.select()

        def _getAllCheckboxes(self):
            '''
            returns all checkbox objects
            '''
            checkboxes = []
            for thing in dir(self):
                thingAsObj = getattr(self, thing)
                if isinstance(thingAsObj, tk.Checkbutton):   
                    checkboxes.append(thingAsObj)

            return checkboxes

        def _getInstallCommandList(self):
            '''
            get list of commands to run to install the selected apps
            '''
            retList = []
            for checkbox in self._getAllCheckboxes():
                if checkbox.checked.get():
                    cmd = '%s install %s -y' % (getChoco(), APPS[checkbox.cget('text')])
                    retList.append(cmd)

            return retList

        def installSelected(self):
            '''
            installs all selected 
            '''
            installCommands = self._getInstallCommandList()
            with self.busyCursor():
                for i in installCommands:
                    print ("About to execute: %s" % i)
                    os.system(i)

                print ("Done")

    ensureHasChoco()
    g = Gui()