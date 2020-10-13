# linx-pyclient
![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-7986cb?style=flat-square)
![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-26a69a?style=flat-square)


A lightweight CLI for uploading and managing your files on a [**linx-server**](https://github.com/andreimarcu/linx-server) instance.

# Usage
```shell script
Usage: linx.py [OPTIONS] COMMAND [ARGS]...

Options:
  --working-dir TEXT  Manually sets the working directory. Any relative
                      argument paths use this as the base.

  -v, --verbose       Print more information
  --config TEXT       Set the custom configuration file
  --version
  --help              Show this message and exit.

Commands:
  delete (del)  Delete a file with the provided delete key
  info (i)      Show information about a file (expiration, size, ...)
  upload (u)    Upload a file
```

See `linx.py <command> --help` for more detailed help.

# Installation

## 1. Prerequisites
[Poetry](https://python-poetry.org/) is the dependency manager of choice here, so you need to have it installed. Additionally, this project is compatible with Python 3.8+ (poetry will insist on it).

## 2. (recommended) Install script
The simplest way to install `linx-pyclient` is to use the provided install script.

Bash and compatible shells:
```shell script
curl -sSL https://raw.githubusercontent.com/DefaultSimon/linx-pyclient/master/scripts/install_linx-pyclient.py | python -
```

On Windows with Powershell
```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/DefaultSimon/linx-pyclient/master/scripts/install_linx-pyclient.py -UseBasicParsing).Content | python -
```

## 2. (advanced, for portable installs)
Clone this repository to a location of your choosing. Next, execute `poetry install` in the root directory. After Poetry is done, add the root directory to your path.

Now, depending on your platform, use `linx.sh` or `linx.ps1` as a "proxy" for the installation (call normally, e.g. `linx.sh --help`).

## 3. Configuration
Before you start using, you must copy and rename the provided example configuration file. Fill out `linx_instance_url` and `linx_api_key`.
