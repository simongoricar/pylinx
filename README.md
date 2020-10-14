# pylinx <sub>a <a href="https://github.com/andreimarcu/linx-server">linx-server</a> CLI</sub>
![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-7986cb?style=flat-square&logo=python&logoColor=white)
![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-689f38?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAcCAYAAABlL09dAAAEsmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS41LjAiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgZXhpZjpQaXhlbFhEaW1lbnNpb249IjIyIgogICBleGlmOlBpeGVsWURpbWVuc2lvbj0iMjgiCiAgIGV4aWY6Q29sb3JTcGFjZT0iMSIKICAgdGlmZjpJbWFnZVdpZHRoPSIyMiIKICAgdGlmZjpJbWFnZUxlbmd0aD0iMjgiCiAgIHRpZmY6UmVzb2x1dGlvblVuaXQ9IjIiCiAgIHRpZmY6WFJlc29sdXRpb249IjcyLjAiCiAgIHRpZmY6WVJlc29sdXRpb249IjcyLjAiCiAgIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiCiAgIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIuMSIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjAtMTAt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)


A lightweight CLI for uploading and managing your files on a [**linx-server**](https://github.com/andreimarcu/linx-server) instance.

# Usage
```shell script
Usage: pylinx [OPTIONS] COMMAND [ARGS]...

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

See `pylinx <command> --help` for more detailed help.

# Installation

## 1. Prerequisites
[Poetry](https://python-poetry.org/) is the dependency manager of choice here, so you need to have it installed (or, if you really don't want to use it, see **b) Pip install**). Additionally, this project is compatible with Python 3.8+ (poetry will insist on it).

## 2. Installation
### a) Install script <sub>(recommended)</sub>
The simplest way to install `pylinx` is to use the provided install script. 
This will create a local virtualenv using [Poetry](https://python-poetry.org/) to avoid polluting your global package list.

Bash and compatible shells:
```shell script
curl -sSL https://raw.githubusercontent.com/DefaultSimon/linx-pyclient/master/scripts/install_linx-pyclient.py | python -
```

On Windows with Powershell
```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/DefaultSimon/linx-pyclient/master/scripts/install_pylinx.py -UseBasicParsing).Content | python -
```

You will still be asked to add the resulting path to your `PATH` variable manually.

### b) Pip install
In cases where other methods are unavailable or fail, you can install pylinx using either

`python -m pip install pylinx` or 
`python -m pip install git+https://github.com/DefaultSimon/linx-pyclient.git`

Do note that this will install packages to your global install, so other methods using Poetry might be preffered.

### c) "Portable Install" <sub>(advanced)</sub>
Clone this repository to a location of your choosing. Next, execute `poetry install` in the root directory. After Poetry is done, add the root directory to your `PATH` variable.

Now, depending on your platform, use `pylinx.sh` or `pylinx.ps1` as a "proxy" for the installation (call normally, e.g. `linx.sh --help`).

## 3. Configuration
Before you start using the CLI, you must copy and rename the provided example configuration file. Fill out `linx_instance_url` and `linx_api_key` (corresponds to `authfile` on the [server](https://github.com/andreimarcu/linx-server)).

You can also do this by simply calling ``