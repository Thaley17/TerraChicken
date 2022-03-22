import typer
import os
import functions
import create
import delete
import list

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




if __name__ == "__main__":
    app()
