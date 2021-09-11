'''
Home to string constants for cAppInstaller
'''

ADD_ADMIN_CMD_PROMPT_VIA_SHIFT_RIGHT_CLICK_REG = r'''Windows Registry Editor Version 5.00

; Created by: Shawn Brink
; Adapted by Charles Machalow
; Note: We're using an older version of this (from wayback machine) since for whatever reason it seems to work better
;  The new one seems to flash a console window, before opening while this one doesn't.
; http://www.sevenforums.com
; Tutorial: http://www.sevenforums.com/tutorials/47415-open-command-window-here-administrator.html

[-HKEY_CLASSES_ROOT\Directory\shell\runas]
[HKEY_CLASSES_ROOT\Directory\shell\runas]
@="Open command window here as Administrator"
"Extended"=""
"HasLUAShield"=""
[HKEY_CLASSES_ROOT\Directory\shell\runas\command]
@="cmd.exe /s /k pushd \"%V\""
[-HKEY_CLASSES_ROOT\Directory\Background\shell\runas]
[HKEY_CLASSES_ROOT\Directory\Background\shell\runas]
@="Open command window here as Administrator"
"Extended"=""
"HasLUAShield"=""
[HKEY_CLASSES_ROOT\Directory\Background\shell\runas\command]
@="cmd.exe /s /k pushd \"%V\""
[-HKEY_CLASSES_ROOT\Drive\shell\runas]
[HKEY_CLASSES_ROOT\Drive\shell\runas]
@="Open command window here as Administrator"
"Extended"=""
"HasLUAShield"=""
[HKEY_CLASSES_ROOT\Drive\shell\runas\command]
@="cmd.exe /s /k pushd \"%V\""
[-HKEY_CLASSES_ROOT\LibraryFolder\background\shell\runas]
[HKEY_CLASSES_ROOT\LibraryFolder\background\shell\runas]
"Extended"=""
"HasLUAShield"=""
@="Open command window here as Administrator"
[HKEY_CLASSES_ROOT\LibraryFolder\background\shell\runas\command]
@="cmd.exe /s /k pushd \"%V\""
; To allow mapped drives to be available in command prompt
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System]
"EnableLinkedConnections"=dword:00000001
'''

INSTALL_CHOCO_CMD = r'''@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"'''