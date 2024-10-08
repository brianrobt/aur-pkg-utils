"""This module provides the AUR Package Utils CLI."""

from typing import Optional

import typer

from aurpkgutils import __app_name__, __version__, aurpkgutils

app = typer.Typer()


@app.command()
def check() -> None:
    aurpkgutils.check()


@app.command()
def init() -> None:
    typer.secho("Initialized aurpkgutils")


def _version_callback(value: bool) -> None:

    if value:

        typer.echo(f"{__app_name__} v{__version__}")

        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:

    return


# def get_latest() -> aurpkgutils.AurPkgUtils:
#     return aurpkgutils.AurPkgUtils()
