import typer
import functions
import utils
import time
import os 

app = typer.Typer()

@app.command()
def local(name: str = typer.Option(None, show_default=False)):
    if name == None:
        name = str(typer.prompt("Enter a Name of the workspace: "))
        functions.createLocalWorkspace(name)
        ws_id = functions.getWsId(name)
        ws_id_formatted = typer.style(f"{ws_id}", fg=typer.colors.GREEN)
        typer.echo(f"Workspace ID:" + ws_id_formatted)
        time.sleep(1)
    else:
      functions.createLocalWorkspace(name)
      ws_id = functions.getWsId(name)
      ws_id_formatted = typer.style(f"{ws_id}", fg=typer.colors.GREEN)
      typer.echo(f"Workspace ID:" + ws_id_formatted)
      time.sleep(1)

@app.command()
def vcs(name: str = typer.Option(None, show_default=False), create_repo: str = typer.Option("y")):
    if name == None:
        name = str(typer.prompt("Enter a Name of the workspace: "))
    else:
        pass
    create_repo = typer.prompt("Create a new VCS Repo for this workspace? (y/n): ")
    if create_repo == "y":
        repo_name = str(typer.prompt("Enter Name for New Repo: "))
        repo_url = functions.createRepoObject(repo_name)# creates repo and returns url
        repo_url_formatted = typer.style(repo_url, fg=typer.colors.GREEN)
        typer.echo(f"Created Github Repo: {repo_url_formatted}")
    else: 
        account = str(typer.prompt("Enter name of account or organization: "))
        repo = str(typer.prompt("Enter the name of the Repo you want to use: "))
        repo_url = "f{account}/{repo}"
        typer.echo(repo_url)
    functions.createVcsWorkspace(name, "1.1.3", repo_url)
    ws_id = functions.getWsId(name)
    ws_id_formatted = typer.style(f"{ws_id}", fg=typer.colors.GREEN)
    typer.echo(f"Workspace ID:" + ws_id_formatted)
    time.sleep(1)
        

if __name__ == "__main__":
    app()