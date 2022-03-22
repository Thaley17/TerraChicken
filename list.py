import typer
import functions

app = typer.Typer()

@app.command("workspaces")
def list():
    functions.listWorkspaces()

@app.command("repos")
def list():
    functions.listAllRepo()