## Proxy for the python script
# If you prefer this, you can add linx.ps1 to your PATH and execute it with any
# arguments as if you were calling the script directly

$originalLocation = $PWD
# Move into the script directory
Set-Location $PSScriptRoot

try {
    # Run the script inside a poetry shell
    poetry run python ./pylinx/linx.py --working-dir $originalLocation @args
} finally {
    Set-Location $originalLocation
}
