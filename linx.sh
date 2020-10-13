#!/usr/bin/env bash
## Proxy for the python script to run inside a virtualenv

# Save the caller current directory and find the script directory
ORIGINALDIR=$PWD
SCRIPTDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

cd $SCRIPTDIR
# Run from the root directory of your installation
poetry run python ./pylinx/linx.py --working-dir "$ORIGINALDIR" --config %linxpath%/config/linxConfig.toml "$@" || :
# Return back to the original directory
cd $ORIGINALDIR
