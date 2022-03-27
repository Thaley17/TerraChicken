import typer
import functions

app = typer.Typer()

@app.command("workspaces")
def list():
    """
    List all Terraform Cloud Workspaces

    Context:
    Workspace ID : Workspace Name : Execution Mode
    """
    functions.listWorkspaces()

@app.command("repos")
def list():
    """
    List all Github Repos under User Account
    """
    functions.listAllRepo()