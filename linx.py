#! python3
import os
import logging
from json import loads
from urllib.parse import urljoin
import datetime

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import pyperclip
import magic
from click import command, echo, style, option, argument, getchar, progressbar, group
from hurry.filesize import size

from linxcore.utilities import Integer
from linxcore.config import API_KEY, INSTANCE_URL, DEFAULT_DELETE_KEY, SCRIPT_DIR


__version__ = "0.1.0"

CMD_UPLOAD_WIDTH = 72
CMD_INFO_WIDTH = 72
CMD_DELETE_WIDTH = 56

#################
# Logging
#################

log = logging.getLogger("LinxPython")
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(SCRIPT_DIR, "logs/linx.log"))
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

log.addHandler(fh)


#################
# Commands
#################
@group()
def cli():
    pass


@command(name="upload")
@option("--randomize", "-r",
        default="no", help="whether to randomize the file name", show_default=True)
@option("--expiry-days", "-e",
        default=30, help="for how many days should the file be retained", show_default=True)
@option("--delete-key", "-d",
        default=DEFAULT_DELETE_KEY, help="what the delete key should be", show_default=True)
@option("--access-key", "-a",
        default=None, help="what the access key (file password) should be", show_default=True)
@argument("file_path")
def linx_upload(randomize: str, expiry_days: int, delete_key: str, access_key: str, file_path: str):
    log.debug("Mode: UPLOAD")
    echo(style("**** Mode: UPLOAD ****".center(CMD_UPLOAD_WIDTH), bold=True, underline=True))

    full_path = os.path.abspath(os.path.join(os.curdir, file_path))
    file_name = os.path.basename(full_path)
    randomize = "yes" if randomize.lower() == "yes" else "no"
    expiry_sec = expiry_days * 24 * 60 * 60

    echo("** Please confirm this configuration **\n".center(CMD_UPLOAD_WIDTH))
    echo()
    echo(f"\tFull file path: \t" + style(full_path, fg="bright_black"))
    echo(f"\tRandomize file name: \t" + style(randomize, fg="bright_black"))
    echo(f"\tExpire in: \t\t" + style(f"{expiry_days} days ({expiry_sec} seconds)", fg="bright_black"))
    echo(f"\tDelete key: \t\t" + style(delete_key, fg="bright_black"))
    echo(f"\tAccess key: \t\t" + style(access_key, fg="bright_black"))
    echo("\n")

    echo("Continue? [y/n] ".center(CMD_UPLOAD_WIDTH), nl=False)
    char = getchar().lower()
    echo()

    if char != "y":
        echo(style("Exiting.", bold=True))
        return

    full_headers = {
        # Auth and options
        "Linx-Api-Key": API_KEY,
        "Linx-Randomize": randomize,
        "Linx-Delete-Key": delete_key,
        "Linx-Access-Key": access_key,
        "Linx-Expiry": str(expiry_sec),
        # other
        "Accept": "application/json",
    }

    file_upload = open(full_path, "rb")
    log.debug(f"Uploading file \"{os.path.basename(full_path)}\" to instance {INSTANCE_URL}")
    log.debug(f"Linx-Randomize: {randomize} | Linx-Delete-Key: {delete_key} "
              f"| Linx-Access-Key: {access_key} | Linx-Expiry: {expiry_sec} ({expiry_days} days)")

    file_content_type = magic.Magic(mime=True).from_file(file_path)
    mp = MultipartEncoder(
        fields={"file": (file_name, file_upload, file_content_type)}
    )

    with progressbar(length=mp.len) as bar:
        last_bytes_read = Integer(0)

        def progress_callback(mon: MultipartEncoderMonitor):
            new_bytes_read = mon.bytes_read
            how_many_uploaded = new_bytes_read - last_bytes_read.get()
            last_bytes_read.set(new_bytes_read)

            bar.update(how_many_uploaded)

        monitor = MultipartEncoderMonitor(mp, progress_callback)

        resp = requests.post(
            url=urljoin(INSTANCE_URL, "upload"), data=monitor,
            headers={**full_headers, **{"Content-Type": mp.content_type}}
        )

        file_upload.close()

        if resp.status_code != 200:
            log.debug(f"Something went wrong, status code is {resp.status_code} and content '{resp.content}'")
            echo(f"Something went wrong, status code is {resp.status_code} and content '{resp.content}'")
            return

        data = loads(resp.content)

        file_url = data.get("url")
        direct_url = data.get("direct_url")

        log.debug(f"File uploaded | url: {file_url} | direct url: {direct_url}")

        echo("\n")
        echo(style("== File uploaded! ==".center(CMD_UPLOAD_WIDTH), bold=True))
        echo()
        echo(style(f"\tFile url: \t\t{file_url}", fg="bright_green"))
        echo(style(f"\tDirect url: \t\t{direct_url}", fg="green"))

        echo()
        echo("Copy direct url to clipboard? [y/n] ", nl=False)
        char = getchar().lower()
        echo()

        if char == "y":
            log.debug("Copied URL to clipboard.")
            pyperclip.copy(direct_url)


@command(name="info")
@argument("file_name")
def linx_info(file_name: str):
    log.debug("Mode: INFO")
    echo(style("**** Mode: INFO ****".center(CMD_INFO_WIDTH), bold=True, underline=True))

    full_url = urljoin(INSTANCE_URL, file_name)
    headers = {
        "Accept": "application/json",
    }

    log.debug(f"Querying info about file: '{file_name}'")

    resp = requests.get(full_url, headers=headers)

    if resp.status_code == 404:
        echo()
        echo(style(f"File does not exist or has expired.".center(CMD_INFO_WIDTH), fg="bright_red"))
        return

    elif resp.status_code != 200:
        echo(style(f"Error, status code is {resp.status_code}"))
        echo(f"Content: {bytes(resp.content).decode('utf-8')}")
        return

    data = loads(resp.content)

    date_now = int(datetime.datetime.now().timestamp())
    expiry = int(data.get("expiry"))

    expiry_days = round((expiry - date_now) / (24 * 60 * 60), 1)

    mime = data.get("mimetype")
    sha256sum = data.get("sha256sum")

    size_raw = int(data.get("size"))
    size_human = size(size_raw)

    log.debug(f"File info | expiry epoch: {expiry} | mime: {mime} | sha256: {sha256sum} | size: {size_raw} bytes ({size_human})")

    echo(style(f"** FILE: {file_name} **".center(CMD_INFO_WIDTH), bold=True))
    echo()
    echo(f"\tExpires in:\t" + style(f"{expiry_days} days", fg="bright_black"))
    echo(f"\tMIME type:\t" + style(mime, fg="bright_black"))
    echo(f"\tSize:\t\t" + style(size_human, fg="bright_black"))
    echo(f"\tSHA256:\t\t" + style(sha256sum, fg="bright_black"))
    echo()


@command(name="delete")
@argument("file_name")
# TODO should this take the default if none if provided?
@argument("delete_key")
def linx_delete(file_name: str, delete_key: str):
    log.debug("Mode: DELETE")
    echo(style("**** Mode: DELETE ****".center(CMD_DELETE_WIDTH), bold=True, underline=True))

    full_url = urljoin(INSTANCE_URL, file_name)
    headers = {
        "Linx-Api-Key": API_KEY,
        "Linx-Delete-Key": delete_key,
        "Accept": "application/json",
    }

    echo()
    echo("Are you sure you want to continue? [y/n] ", nl=False)
    char = getchar().lower()
    echo()

    if char != "y":
        echo(style("Exiting.", bold=True))
        return

    log.debug(f"Deleting file '{file_name}' with delete key '{delete_key}'")
    resp = requests.delete(full_url, headers=headers)

    decoded_content = bytes(resp.content).decode("utf-8")
    was_deleted = resp.status_code == 200 and decoded_content == "DELETED"

    if was_deleted:
        echo()
        echo(style(f"File \"{file_name}\" was deleted.".center(CMD_DELETE_WIDTH), fg="bright_green", bold=True))

        log.debug("File deleted.")
    else:
        echo()
        echo(style(f"Could not delete file.".center(CMD_DELETE_WIDTH), fg="bright_red", bold=True))
        echo(style(f"Status code: {resp.status_code}".center(CMD_DELETE_WIDTH), fg="bright_black"))

        log.debug(f"File could not be deleted (status {resp.status_code})")


cli.add_command(linx_upload)
cli.add_command(linx_info)
cli.add_command(linx_delete)
#################
# Run the appropriate command
#################
if __name__ == '__main__':
    cli()
