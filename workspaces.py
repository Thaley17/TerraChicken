import typer
import functions
import time
import os 
import json

app = typer.Typer()

TFC_ORGANIZATION = "devhop"

"""
Module creates Local Terraform Cloud Workspace. Also returns Workspace ID

--out exports payload.json. --generate/-g: Generates Terraform Block Config
"""
@app.command()
def local(name: str = typer.Option(None, "--name" , "-n") , generate: bool = 
        typer.Option(False, "--generate/--no-generate", "-g/-G") , out: bool =
        typer.Option(False, "--out/--in" , "-o/-O")):
    if name == None:
        name = str(typer.prompt("Enter a Name of the workspace: "))
    else:
        pass
    payload = functions.createLocalWorkspace(name)
    ws_id = functions.getWsId(name)
    ws_id_formatted = typer.style(f"{ws_id}", fg=typer.colors.GREEN)
    typer.echo(f"Workspace ID:" + ws_id_formatted)
    if generate:
        functions.createTerraformBlock("cli", name, TFC_ORGANIZATION)
    else:
        pass
    if out:
        with open("payload.json" , "w") as f:
            json.dump(payload, f, indent=2, sort_keys=True)
    else:
        pass
    time.sleep(1)

"""
Creates VCS Backed Workspace. Gives user the chance to create or BYO(Repo).

 --out exports payload.json. --generate/-g: Generates Terraform Block Config 
"""
@app.command()
def vcs(name: str = typer.Option(None, "--name" , "-n"), create_repo: str = typer.Option("y") , generate: bool = 
        typer.Option(False, "--generate/--no-generate", "-g/-G") , out: bool =
        typer.Option(False, "--out/--in" , "-o/-O")):
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
    payload = functions.createVcsWorkspace(name, "1.1.3", repo_url)
    ws_id = functions.getWsId(name)
    ws_id_formatted = typer.style(f"{ws_id}", fg=typer.colors.GREEN)
    typer.echo(f"Workspace ID:" + ws_id_formatted)
    if generate:
        tfVersion = functions.terraformVersion()
        if tfVersion >= 1.1: # The cloud meta block wasn't implemented until v1.1.0
            functions.createTerraformBlock("vcs", name, TFC_ORGANIZATION)
        else:
            typer.secho("Your Terraform Version cannot support the Cloud meta block. Upgrade to v1.1 or newer!" , fg=typer.colors.YELLOW)
    if out:
        with open("payload.json" , "w") as f:
            json.dump(payload, f, indent=2, sort_keys=True)
    else:
        pass
    time.sleep(1)
        

if __name__ == "__main__":
    app()