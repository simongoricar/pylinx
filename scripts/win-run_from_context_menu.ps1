# NOTE: DO NOT CALL THIS SCRIPT DIRECTLY

## This script properly formats the shell and calls pylinx to upload the file
# from the context menu

[console]::WindowWidth = 100
[console]::WindowHeight = 24
[console]::BufferWidth = [console]::WindowWidth
$host.ui.RawUI.WindowTitle = "pylinx"

$originalLocation = $PWD
# Move into the script directory
Set-Location $PSScriptRoot

try {
    if ($args[0] -eq "-usePortable") {
        # Run the script inside a poetry shell
        $flag, $otherArgs = $args;
        poetry run python ../pylinx/linx.py --working-dir $originalLocation --config %linxpath%/config/linxConfig.toml @otherArgs
    } elseif ($args[0] -eq "-useBinary") {
        # TODO document and use this in win-add_to_context_menu.py
        $flag, $otherArgs = $args;
        pylinx @otherArgs
    } else {
        $pylinxBin = "$(poetry env info -p -n)\Scripts\pylinx.exe"
        & $pylinxBin @args
    }
} finally {
    Write-Output ""
    Read-Host -Prompt "Press enter to exit"
    Set-Location $originalLocation
}
