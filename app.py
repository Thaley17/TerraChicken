import typer
import time
import os
import functions
import utils
import repo
import workspaces 

app = typer.Typer()
app.add_typer(workspaces.app, name="create")
app.add_typer(repo.app, name="repo")

TC_MODE = os.getenv("TC_MODE", None)

dev_mode_enabled = False

while TC_MODE == "Dev" or "DEV":
    dev_mode_enabled = True
    typer.secho(f"Development Mode" , fg=typer.colors.YELLOW , bold=True)
    break


@app.command()
def list():
    functions.listWorkspaces()

@app.command()
def remove(ws_name: str = ""):
    functions.listWorkspaces()
    ws_name = str.lower(input("Enter the name of Workspace(s): ")).split()
    for name in ws_name:
        try:
            functions.deleteWorkspaces(name)
        except:
            print(f"\n{utils.bcolors.WARNING}{name}{utils.bcolors.ENDC} not found in active Workspaces.")
        finally:
            typer.echo("Remaining Workspaces:")
            functions.listWorkspaces()

if __name__ == "__main__":
    app()
