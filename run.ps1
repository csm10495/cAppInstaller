$ErrorActionPreference = "Stop"

function IsAdmin() {
	<#
	IsAdmin() - Returns $TRUE if the script is being run as an admin
	#>
	return ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
}

function HasChoco() {
    <#
    HasChoco() - Returns $TRUE if the system has chocolatey
    #>

    try {
        Get-Command choco   
    }
    catch {
        return $FALSE  
    }
    return $TRUE
}

function HasPython() {
    <#
    HasPython() - Returns $TRUE if the system has Python
    #>
    try {
        Get-Command python   
    }
    catch {
        return $FALSE  
    }
    return $TRUE
}

function RefreshPath() {
    <#
    RefreshPath() - Refreshes the system path
    #>
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

if (IsAdmin) { # Make sure we have admin
    if (-Not (HasChoco)) {
        Write-Output "Installing choco"
        [System.Net.WebRequest]::DefaultWebProxy.Credentials = [System.Net.CredentialCache]::DefaultCredentials; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    } else {
        Write-Output "Detected choco"
    } 

    Write-Output "Turning off Global Confirmation in choco"
    choco feature enable -n allowGlobalConfirmation
    
    if (-Not (HasPython)) {
        Write-Output "Installing Python"
        choco install python2 /InstallDir "C:\Python27"
    } else {
        Write-Output "Detected Python"
    } 

    RefreshPath

    python ((Split-Path $script:MyInvocation.MyCommand.Path) + "/gui.py")
} else {
    Write-Error "Didn't detect admin... please rerun as admin"
}