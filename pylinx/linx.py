import sys
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import logging
from json import loads
from urllib.parse import urljoin
import datetime
from shutil import copy2

from magic import from_file
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import pyperclip
from click import echo, style, option, argument, getchar, progressbar, group, pass_context, Context, edit
# noinspection PyProtectedMember
from click._termui_impl import WIN
from click_aliases import ClickAliasedGroup
from hurry.filesize import size

from pylinx.linxcore.utilities import Integer, generate_random_pass
from pylinx.linxcore.config import ROOT_DIR, PROJECT_VERSION, load_config, LinxConfig

CMD_SETUP_WIDTH = 72
CMD_UPLOAD_WIDTH = 72
CMD_INFO_WIDTH = 72
CMD_DELETE_WIDTH = 56

#################
# Logging
#################

log = logging.getLogger("LinxPython")
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(ROOT_DIR, "./logs/linx.log"))
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

log.addHandler(fh)


def edit_file(file_name: str):
    # This fixes handling of editors on windows
    # click doesn't properly handle spaces in editor installation paths,
    # so we force notepad
    if WIN:
        return edit(editor="notepad", filename=file_name)
    else:
        return edit(filename=file_name)


def print_version(ctx: Context, _, value):
    if not value or ctx.resilient_parsing:
        return

    echo(f"linx-pyclient version: {PROJECT_VERSION}")
    ctx.exit()


@group(cls=ClickAliasedGroup)
@option("--working-dir",
        default=os.curdir,
        help="Manually sets the working directory. Any relative argument paths use this as the base.")
@option("-v", "--verbose", is_flag=True, help="Print more information")
@option("--config", default=None, help="Set the custom configuration file")
@option("--version", is_flag=True, is_eager=True, expose_value=False, callback=print_version)
# TODO -y option to skip prompts
@pass_context
def cli(ctx: Context, working_dir: str, verbose: bool, config: str):
    # Pass the working_dir in a Context to other commands
    ctx.ensure_object(dict)
    ctx.obj["working_dir"] = working_dir
    ctx.obj["verbose"] = verbose
    ctx.obj["configFile"] = config

    # Don't throw configuration errors on `pylinx setup`
    if ctx.invoked_subcommand != "setup":
        ctx.obj["config"] = load_config(config)

    if verbose:
        echo(f"Working directory: '{working_dir}'")


#################
# Commands
#################
@cli.command(name="configure", help="Manage your configuration")
@pass_context
def linx_config(ctx: Context):
    working_dir = ctx.obj['working_dir']

    log.debug("Mode: CONFIGURE")
    echo(style("**** Mode: CONFIGURE ****".center(CMD_SETUP_WIDTH), bold=True, underline=True))

    def get_choice(choices: list) -> str:
        choice = getchar(echo=True).lower()
        echo()

        if choice not in choices:
            echo(style("Invalid choice.", fg="bright_red"))
            return ctx.exit()

        if choice == "c":
            echo("Cancelled.")
            return ctx.exit()

        return choice

    # Ask the user for the action
    echo()
    echo("What would you like to do?")
    echo(style("\t1) ", fg="bright_green") + "Generate an empty configuration")
    echo(style("\t2) ", fg="bright_green") + "Interactively generate a new configuration")
    echo(style("\t3) ", fg="bright_green") + "Edit your current confguration")
    echo()
    echo(style("Please choose [1/2/[C]ancel]: ", fg="bright_black"), nl=False)

    choice_what = get_choice(["1", "2", "3", "c"])

    # Ask the user for the location
    echo("\n")
    echo("Where would you like to place it?" if choice_what != "3" else "Which one would you like to edit?")
    echo(style("\t1) ", fg="bright_green") + "Current directory")
    echo(style("\t2) ", fg="bright_green") + "User home directory (~/.config/pylinx/linxConfig.toml)")
    echo(style("\nIf you are not sure what to choose, choose \"2) User home directory\".", fg="bright_black"))
    echo()
    echo(style("Please choose [1/2/[C]ancel]: ", fg="bright_black"), nl=False)

    choice_where = get_choice(["1", "2", "c"])

    # Parse destination
    if choice_where == "1":
        config_file_destination = os.path.realpath(os.path.join(working_dir, "linxConfig.toml"))
    elif choice_where == "2":
        config_file_destination = os.path.realpath(
            os.path.join(os.path.expanduser("~"), ".config/pylinx/linxConfig.toml")
        )
    else:
        return ctx.exit()

    # Ask for confirmation if it already exists
    if os.path.isfile(config_file_destination) and choice_what != "3":
        echo(f"\nThis configuration file "
             + style(f"('{config_file_destination}')", fg="bright_black")
             + " already exists.\n")
        echo(style("Do you want to edit the current one instead? [[E]dit/[[O]verwrite]] ", fg="bright_white"), nl=False)

        choice_overwrite = getchar(echo=True).lower()
        echo()
        if choice_overwrite == "e":
            echo("Opening an editor - save and close when done.")
            edit_file(config_file_destination)
            echo("Editor closed, exiting.")
            return ctx.exit()
        elif choice_overwrite == "o":
            pass
        else:
            echo(style("Invalid choice.", fg="bright_red"))
            return ctx.exit()

    if choice_what == "1" or choice_what == "2":
        # Make sure an empty configuration exists
        config_file_example = os.path.realpath(os.path.join(ROOT_DIR, "config/linxConfig.EXAMPLE.toml"))
        if not os.path.isfile(config_file_example):
            echo(style("Could not generate an empty configuration: missing files - bad install", fg="bright_red"))
            return ctx.exit(1)

        if choice_what == "1":
            # Generate an empty configuration
            echo(f"Copying blank configuration to '{config_file_destination}'")
            copy2(config_file_example, config_file_destination)

            echo("Blank configuration copied.")

        elif choice_what == "2":
            # Interactively generate a new configuration
            echo(f"Copying blank configuration to '{config_file_destination}'")
            copy2(config_file_example, config_file_destination)

            echo("Opening an editor - save and close when done.")
            edit_file(config_file_destination)
            echo("Editor closed, exiting.")
    elif choice_what == "3":
        if not os.path.isfile(config_file_destination)

        echo("Opening an editor - save and close when done.")
        edit_file(config_file_destination)
        echo("Editor closed, exiting.")


@cli.command(name="upload", aliases=["u"], help="Upload a file")
@option("--randomize", "-r", is_flag=True, help="whether to randomize the file name", show_default=True)
@option("--expiry-days", "-e",
        default=30, help="for how many days should the file be retained (maximum is set by the server!)",
        show_default=True)
@option("--delete-key", "-d",
        default=None, help="what the delete key should be [default: random]")
@option("--access-key", "-a",
        default=None, help="what the access key (file password) should be", show_default=True)
@option("--filename", "-f",
        default=None, help="custom filename [default: same as file]")
@argument("file_path", type=str)
@pass_context
def linx_upload(ctx: Context, randomize: str, expiry_days: int,
                delete_key: str, access_key: str, file_path: str, filename: str):
    """
    Upload the provided file.
    """
    working_dir = ctx.obj['working_dir']
    config: LinxConfig = ctx.obj["config"]
    is_verbose: bool = ctx.obj["verbose"]

    if delete_key is None:
        if is_verbose:
            echo("No --delete-key passed, generating random one.")

        delete_key = generate_random_pass(16)

    log.debug("Mode: UPLOAD")
    echo(style("**** Mode: UPLOAD ****".center(CMD_UPLOAD_WIDTH), bold=True, underline=True))

    full_path = os.path.abspath(os.path.join(working_dir, file_path))
    file_name = filename if filename is not None else os.path.basename(full_path)
    file_content_type = from_file(full_path, mime=True)

    randomize = "yes" if randomize is True else "no"
    expiry_sec = expiry_days * 24 * 60 * 60

    echo("** Please confirm this configuration **\n".center(CMD_UPLOAD_WIDTH))
    echo()
    echo(f"\tFull file path: \t" + style(full_path, fg="bright_black"))
    echo(f"\tRandomize file name: \t" + style(randomize, fg="bright_black"))
    echo(f"\tFile name:\t\t" + style(f"{file_name} ({file_content_type})", fg="bright_black"))
    echo(f"\tExpire in: \t\t" + style(f"{expiry_days} days ({expiry_sec} seconds)", fg="bright_black"))
    echo(f"\tDelete key: \t\t" + style(delete_key, fg="bright_black"))
    echo(f"\tAccess key: \t\t" + style(str(access_key), fg="bright_black"))
    echo("\n")

    echo("Continue? [y/n] ".center(CMD_UPLOAD_WIDTH), nl=False)
    char = getchar(echo=True).lower()
    echo()

    if char != "y":
        echo(style("Exiting.", bold=True))
        return

    full_headers = {
        # Auth and options
        "Linx-Api-Key": config.API_KEY,
        "Linx-Randomize": randomize,
        "Linx-Delete-Key": delete_key,
        "Linx-Expiry": str(expiry_sec),
        # other
        "Accept": "application/json",
    }
    if access_key is not None:
        full_headers = {
            **full_headers,
            **{
                "Linx-Access-Key": access_key
            }
        }

    file_upload = open(full_path, "rb")
    log.debug(f"Uploading file \"{os.path.basename(full_path)}\" to instance {config.INSTANCE_URL}")
    log.debug(f"Linx-Randomize: {randomize} | Linx-Delete-Key: {delete_key} "
              f"| Linx-Access-Key: {access_key} | Linx-Expiry: {expiry_sec} ({expiry_days} days)")

    mp = MultipartEncoder(
        fields={
            "file": (file_name, file_upload, file_content_type),
            "expires": str(expiry_sec),
            "access_key": str(access_key),
        }
    )

    with progressbar(length=mp.len) as bar:
        last_bytes_read = Integer(0)

        def progress_callback(mon: MultipartEncoderMonitor):
            new_bytes_read = mon.bytes_read
            how_many_uploaded = new_bytes_read - last_bytes_read.get()
            last_bytes_read.set(new_bytes_read)

            bar.update(how_many_uploaded)

        monitor = MultipartEncoderMonitor(mp, progress_callback)

        try:
            req = requests.Request(
                method="POST", url=urljoin(config.INSTANCE_URL, "upload"), data=monitor,
                headers={**full_headers, **{"Content-Type": mp.content_type}}
            )
            prep = req.prepare()

            if is_verbose:
                formatted_headers = "\n".join(f"{k}: {v}" for k, v in prep.headers.items())
                # noinspection PyUnresolvedReferences
                echo(f"Sending HTTP POST request:"
                     f"\n{'=' * 10}\n"
                     f"{prep.method} {prep.url}\n"
                     f"{formatted_headers.replace(config.API_KEY, '[REDACTED]')}\n\n"
                     f"[multipart-form length: {prep.body.len}]\n\n"
                     f"{'=' * 10}")

            resp = requests.session().send(prep)
        except requests.ConnectionError as e:
            echo(style("Could not send the request.", fg="bright_red"))
            if is_verbose:
                echo(f"requests.ConnectionError: '{e}'")

            return

        file_upload.close()

        if resp.status_code != 200:
            log.error(f"Something went wrong, status code is {resp.status_code} and content '{resp.content}'")

            echo(f"Something went wrong, status code is {resp.status_code}")
            if is_verbose:
                echo(f"Response body: '{resp.content}'\n")

            return

        data = loads(resp.content)

        if is_verbose:
            echo(f"Response JSON: '{data}'\n")

        resp_file_url = data.get("url")
        resp_direct_url = data.get("direct_url")

        resp_access_key = data.get("access_key")
        resp_delete_key = data.get("delete_key")

        log.debug(f"File uploaded | url: {resp_file_url} | direct url: {resp_direct_url}")

        echo("\n")
        echo(style("== File uploaded! ==".center(CMD_UPLOAD_WIDTH), bold=True))
        echo()
        echo(style(f"\tFile url: \t\t{resp_file_url}", fg="bright_green"))
        echo(style(f"\tDirect url: \t\t{resp_direct_url}", fg="green"))
        echo()
        echo(style(f"\tAccess Key: {resp_access_key if resp_access_key != '' else '[None]'} "
                   f"| Delete Key: {resp_delete_key}", fg="bright_black"))

        echo()
        echo("Copy direct url to clipboard? [y/n] ", nl=False)
        char = getchar(echo=True).lower()
        echo()

        if char == "y":
            log.debug("Copied URL to clipboard.")
            pyperclip.copy(resp_direct_url)


@cli.command(name="info", aliases=["i"], help="Show information about a file (expiration, size, ...)")
@argument("file_name")
@pass_context
def linx_info(ctx: Context, file_name: str):
    """
    Show information about the file.
    """
    is_verbose: bool = ctx.obj["verbose"]
    config: LinxConfig = ctx.obj["config"]

    log.debug("Mode: INFO")
    echo(style("**** Mode: INFO ****".center(CMD_INFO_WIDTH), bold=True, underline=True))

    full_url = urljoin(config.INSTANCE_URL, file_name)
    headers = {
        "Accept": "application/json",
    }

    log.debug(f"Querying info about file: '{file_name}'")
    try:
        resp = requests.get(full_url, headers=headers)
    except requests.ConnectionError as e:
        echo(style("Could not send the request.", fg="bright_red"))
        if is_verbose:
            echo(f"requests.ConnectionError: '{e}'")

        return

    if resp.status_code == 404:
        echo()
        echo(style(f"File does not exist or has expired.".center(CMD_INFO_WIDTH), fg="bright_red"))

        if is_verbose:
            echo(f"Response body: '{resp.content}'\n")

        return

    elif resp.status_code != 200:
        echo(style(f"Error, status code is {resp.status_code}"))
        echo(f"Content: {bytes(resp.content).decode('utf-8')}")
        return

    data = loads(resp.content)

    if is_verbose:
        echo(f"Response JSON: '{data}'\n")

    date_now = int(datetime.datetime.now().timestamp())
    expiry = int(data.get("expiry"))

    expiry_days = round((expiry - date_now) / (24 * 60 * 60), 1)

    mime = data.get("mimetype")
    sha256sum = data.get("sha256sum")

    size_raw = int(data.get("size"))
    size_human = size(size_raw)

    log.debug(f"File info | expiry epoch: {expiry} | mime: {mime} "
              f"| sha256: {sha256sum} | size: {size_raw} bytes ({size_human})")

    echo(style(f"** FILE: {file_name} **".center(CMD_INFO_WIDTH), bold=True))
    echo()
    echo(f"\tExpires in:\t" + style(f"{expiry_days} days", fg="bright_black"))
    echo(f"\tMIME type:\t" + style(mime, fg="bright_black"))
    echo(f"\tSize:\t\t" + style(size_human, fg="bright_black"))
    echo(f"\tSHA256:\t\t" + style(sha256sum, fg="bright_black"))
    echo()


@cli.command(name="delete", aliases=["del"], help="Delete a file with the provided delete key")
@argument("file_name")
@argument("delete_key")
@pass_context
def linx_delete(ctx: Context, file_name: str, delete_key: str):
    """
    Delete a file.
    """
    is_verbose: bool = ctx.obj["verbose"]
    config: LinxConfig = ctx.obj["config"]

    log.debug("Mode: DELETE")
    echo(style("**** Mode: DELETE ****".center(CMD_DELETE_WIDTH), bold=True, underline=True))

    full_url = urljoin(config.INSTANCE_URL, file_name)
    headers = {
        "Linx-Api-Key": config.API_KEY,
        "Linx-Delete-Key": delete_key,
        "Accept": "application/json",
    }

    echo()
    echo("Are you sure you want to continue? [y/n] ", nl=False)
    char = getchar(echo=True).lower()
    echo()

    if char != "y":
        echo(style("Exiting.", bold=True))
        return

    log.debug(f"Deleting file '{file_name}' with delete key '{delete_key}'")
    try:
        resp = requests.delete(full_url, headers=headers)
    except requests.ConnectionError as e:
        echo(style("Could not send the request.", fg="bright_red"))
        if is_verbose:
            echo(f"requests.ConnectionError: '{e}'")

        return

    if is_verbose:
        echo(f"Response status {resp.status_code}, content '{resp.content}'")

    decoded_content = bytes(resp.content).decode("utf-8")
    was_deleted = resp.status_code == 200 and decoded_content == "DELETED"

    if was_deleted:
        echo()
        echo(style(f"File \"{file_name}\" was deleted.".center(CMD_DELETE_WIDTH), fg="bright_green", bold=True))

        log.debug("File deleted.")
    else:
        echo()
        echo(style(f"Could not delete file.".center(CMD_DELETE_WIDTH), fg="bright_red", bold=True))

        if resp.status_code == 401:
            echo(style(f"Incorrect delete key!".center(CMD_DELETE_WIDTH), fg="bright_black"))
        else:
            echo(style(f"Status code: {resp.status_code}".center(CMD_DELETE_WIDTH), fg="bright_black"))

        log.debug(f"File could not be deleted (status {resp.status_code})")


#################
# Run the appropriate command
#################
if __name__ == '__main__':
    cli(obj={})
