import typer
import terrachicken.functions as functions

app = typer.Typer()

@app.command("repo")
def delete(name: str = typer.Option(None, "-n")):
    if name == None:
        functions.listAllRepo()
        name = str(typer.prompt("Enter Repo Name to Delete: "))
    else:
        pass
    org = functions.getUserName()
    full_name = f"{org}/{name}"
    typer.confirm(f"Are you sure you want to delete {org}/{name}?" , abort=True )
    functions.deleteRepo(full_name)

@app.command("workspace")
def delete(ws_name: str = ""):
    functions.listWorkspaces()
    ws_name = str.lower(input("Enter the name of Workspace(s): ")).split()
    ws_name_formatted = typer.style(f"{ws_name}", fg=typer.colors.RED)
    for name in ws_name:
        try:
            functions.deleteWorkspaces(name)
        except:
            typer.echo(f"\n {ws_name_formatted} not found in active Workspaces.")
        finally:
            typer.echo("Remaining Workspaces:")
            typer.echo("Exec-Mode  |  Workspace ID  |  Workspace Name")
            functions.listWorkspaces()