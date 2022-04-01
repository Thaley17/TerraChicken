import typer
import terrachicken.functions as functions

app = typer.Typer()

@app.command("workspaces")
def list():
    """
    List all Terraform Cloud Workspaces

    Context:
    Workspace ID : Workspace Name : Execution Mode
    """
    typer.echo("Exec-Mode  |  Workspace ID  |  Workspace Name")
    functions.listWorkspaces()

@app.command("repos")
def list():
    """
    List all Github Repos under User Account
    """
    functions.listAllRepo()