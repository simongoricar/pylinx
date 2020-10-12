# linx-pyclient
![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue)
![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-brightgreen)


A lightweight CLI for uploading and managing your files on a [**linx-server**](https://github.com/andreimarcu/linx-server) instance.


# Installation

## 1. Prerequisites
[Poetry](https://python-poetry.org/) is the dependency manager of choice here, so you need to have it installed. Additionally, this is tested and used on Python 3.8+, but should work on older version down to 3.6, where f-strings were introduced.

## 2. Cloning and Poetry
If you are not sure about what you are doing: skip everything but `3. Configuration` and run `win-install_pylinx_client.ps1` with powershell (prefferably [6+](https://github.com/PowerShell/PowerShell)).

Clone this repository to a location of your choice. Next, execute `poetry install` in the root directory to create a virtualenv and install all necessary dependencies.
If you know what you are doing: you can also use the requirements.txt file if you don't want to use Poetry for some reason.

## 3. Configuration
Copy and rename the provided example configuration file.
Fill out the instance url and api key values.

## 4. Quick access
*(optional, but recommended)* Lastly, set it up for quick access. 
On Windows, you would add the directory to your PATH and then use the provided `linx.ps1` script to call the script from anywhere in the powershell/comand prompt as usual `linx.ps1 upload ...`.

# Usage
```bash
Usage: linx.py [OPTIONS] COMMAND [ARGS]...

Options:
  --working-dir TEXT  Manually sets the working directory. Any relative
                      argument paths use this as the base.

  --verbose           Print more information
  --version
  --help              Show this message and exit.

Commands:
  delete (d)  Delete a file with the provided delete key
  info (i)    Show information about a file (expiration, size, ...)
  upload (u)  Upload a file
```

See `linx.py <command> --help` for subcommand help.