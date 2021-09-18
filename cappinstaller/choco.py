'''
Home to choco-related things for cAppInstaller
'''
import pathlib
import queue
import shlex
import shutil

from .strings import INSTALL_CHOCO_CMD
from .util import subprocess_call_live_output

CHECKBOXES_PER_ROW = 3

CHOCOLATEY_APPS = {
    # Display: Args
    '7-Zip' : '7zip',
    '8GadgetPack' : '8gadgetpack',
    'Adobe Reader' : 'adobereader',
    'API Monitor' : 'apimonitor',
    'Audacity' : 'audacity',
    'Authy' : 'authy-desktop',
    'BGInfo' : 'bginfo',
    'CPU-Z' : 'cpu-z',
    'CrystalDiskInfo' : 'crystaldiskinfo',
    'CrystalDiskMark' : 'crystaldiskmark',
    'DebugView' : 'dbgview',
    'Discord' : 'discord',
    'Epic Games Launcher' : 'epicgameslauncher',
    'Filezilla' : 'filezilla',
    'FurMark' : 'furmark',
    'Git' : 'git --params "/NoAutoCrlf"',
    'Git Extensions': 'gitextensions',
    'Google Chrome': 'googlechrome',
    'GrepWin': 'grepwin',
    'GSmartControl': 'gsmartcontrol',
    'HWiNFO' : 'hwinfo',
    'HxD': 'hxd',
    'Intel CPU Diagnostic ': 'intel-ipdt',
    'KiTTY' : 'kitty',
    'Link Shell Extension': 'linkshellextension',
    'Logitech Gaming' : 'logitechgaming',
    'Minecraft': 'minecraft',
    'Mp3tag' : 'mp3tag',
    'NoMachine': 'nomachine',
    'Notepad Plus Plus': 'notepadplusplus',
    'Open Shell (Classic Shell)': 'open-shell --params "/StartMenu"',
    'Postman': 'postman',
    'Path Copy Copy': 'path-copy-copy',
    'Process Explorer': 'procexp',
    'PuTTY' : 'putty',
    'Python 2': 'python2 /InstallDir "C:/Python27"',
    'Python 3.7': 'python --version 3.7.0 --params "/InstallDir:C:/Python37"',
    'Python 3.8': 'python --version 3.8.0 --params "/InstallDir:C:/Python38"',
    'Python 3.9': 'python --version 3.9.7 --params "/InstallDir:C:/Python39"',
    'Resource Hacker': 'reshack',
    'ScreenToGif': 'screentogif',
    'Skype': 'skype --version 7.41.0.10101',
    'Smartmontools': 'smartmontools',
    'Steam': 'steam',
    'Sudo': 'sudo',
    'Teracopy': 'teracopy',
    'TortoiseHg': 'tortoisehg',
    'Transmission': 'transmission',
    'VirtualBox' : 'virtualbox',
    'Visual Leak Detector' : 'visualleakdetector',
    'Visual Studio Code': 'visualstudiocode',
    'Visual Studio 2017 Community': 'visualstudio2017community visualstudio2017-workload-nativecrossplat visualstudio2017-workload-nativedesktop visualstudio2017-workload-universal windows-sdk-10.1',
    'Visual Studio 2019 Community': 'visualstudio2019community visualstudio2019-workload-nativecrossplat visualstudio2019-workload-nativedesktop visualstudio2019-workload-universal windows-sdk-10.1',
    'Visual Studio 2019 Enterprise': 'visualstudio2019enterprise visualstudio2019-workload-nativecrossplat visualstudio2019-workload-nativedesktop visualstudio2019-workload-universal windows-sdk-10.1',
    'VLC': 'vlc',
    'VNC Viewer': 'vnc-viewer',
    'Windows Terminal': 'microsoft-windows-terminal',
    'Wget' : 'wget',
    'WinDirStat': 'windirstat',
    'WinMerge': 'winmerge',
    'Xming' : 'xming',
}

class Choco:
    '''
    Class for performing operations via Chocolatey
    '''
    # Only do this once per gui run.
    ALLOW_GLOBAL_CONFIRMATION_SET = False

    def __init__(self, display_name: str, output_queue: queue.Queue):
        '''
        The package is actually the package and args string
        The output queue is used to send live output back to the GUI.
        '''
        self.package = shlex.split(CHOCOLATEY_APPS[display_name])
        self.output_queue = output_queue

    def install(self):
        '''
        Attempts to install the given package
        '''
        if not Choco.ALLOW_GLOBAL_CONFIRMATION_SET:
            subprocess_call_live_output(self.output_queue, [
                str(self.get_choco()),
                'feature',
                'enable',
                '-n=allowGlobalConfirmation',
                '-y'
            ])
            Choco.ALLOW_GLOBAL_CONFIRMATION_SET = True

        return subprocess_call_live_output(self.output_queue, [
            str(self.get_choco()),
            'install',
        ] + self.package + [
            '-y'
        ])

    def get_choco(self):
        '''
        Attempts to get back the path to choco.exe, if not available install choco
        then returns the path to choco.exe
        '''
        choco = shutil.which('choco')
        if not choco:
            choco = r"C:\ProgramData\chocolatey\choco.exe"

        choco = pathlib.Path(choco)

        if choco.is_file():
            return choco
        else:
            self.output_queue.put_nowait(['Installing Choco'])
            subprocess_call_live_output(self.output_queue, INSTALL_CHOCO_CMD)
            return self.get_choco()
