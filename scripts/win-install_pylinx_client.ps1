# This script will run a poetry install and add the directory to path
Write-Output "Installing everything, please wait...\n\n"

Set-Location ..

## 1) Install packages with poetry
Write-Output "1) Installing python packages with poetry"
poetry install

## 2) Add to PATH
Write-Output "2) Adding the main directory to PATH..."
$location = Get-Location

Write-Output "For safety, here is your previous PATH:"
Write-Output $Env:Path
Write-Output "Now appending $($location)..."

reg add HKCU\Environment /v PATH /d "%path%;$($location)" /f

Write-Output "done."

Write-Output "DONE INSTALLING. Please (re)open your shell to see the changes."
Write-Output "You can now run the CLI with 'linx.ps1 <parameters>'. "
Write-Output "If not, manually install Powershell 6/7 from https://github.com/PowerShell/PowerShell"
Write-Output ""
Write-Output "If you ever move this directory, please remove the old PATH and virtualenv, then run this script again."