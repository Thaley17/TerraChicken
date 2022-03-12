import typer
import functions
import utils

app = typer.Typer()

@app.command()
def local():
    typer.echo("Better Local Workspace")

@app.command()
def vcs():
    typer.echo("Better VCS Workspace")

if __name__ == "__main__":
    app()