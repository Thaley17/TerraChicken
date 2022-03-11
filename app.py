import typer
import time
import os
import functions

app = typer.Typer()

TC_MODE = os.getenv("TC_MODE", None)

dev_mode_enabled = False

while TC_MODE == "Dev" or "DEV":
    dev_mode_enabled = True
    typer.secho(f"Development Mode" , fg=typer.colors.YELLOW , bold=True)
    time.sleep(1)
    break

@app.command()
def workspace(create: bool , workflow: str = ""):
    if create == True:
        name = str(typer.prompt("Enter a Name of the workspace: "))
        print(type(name))
        functions.createLocalWorkspace(name)
        ws_id = functions.getWsId(name)
        print(type(ws_id))
        print(ws_id)
        ws_id_formatted = typer.style(f"{ws_id}", fg=typer.colors.GREEN)
        typer.echo(f"Workspace ID:" + ws_id_formatted)
        time.sleep(1)   
    else:
        pass

if __name__ == "__main__":
    app()
