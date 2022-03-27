import typer
import os
import create
import delete
import list
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

app = typer.Typer()
app.add_typer(create.app, name="create")
app.add_typer(delete.app, name="delete")
app.add_typer(list.app, name="list")

TC_MODE = os.getenv("TC_MODE", None)

dev_mode_enabled = False

while TC_MODE == "Dev" or "DEV":
    dev_mode_enabled = True
    typer.secho(f"Development Mode" , fg=typer.colors.YELLOW , bold=True)
    break

__version__ = "0.1.0"


@app.command()
def version():
    """
    Prints current version of Terrachicken.
    """
    typer.echo(f"v{__version__}")



if __name__ == "__main__":
    app()
