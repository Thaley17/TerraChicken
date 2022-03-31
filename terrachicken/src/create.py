import typer
import terrachicken.functions as functions
import time
import json

app = typer.Typer()
workspace = typer.Typer()
app.add_typer(workspace, name="workspace")

TFC_ORGANIZATION = "devhop"



@workspace.command()
def local(name: str = typer.Option(None, "--name" , "-n", help="Workspace Name"),
        generate: bool = typer.Option(False, "--generate", "-g" , help="Generates a Terraform Block Configuration"),
        out: bool = typer.Option(False, "--out" , "-o" , help="JSON Output of Workspace payload")
        ):
    """
    Create Terraform Cloud Local Workspace.
    """    
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
@workspace.command()
def vcs(
    name: str = typer.Option(None, "--name" , "-n" , help="Workspace Name"), 
    create_repo: str = typer.Option("y", help="Set Boolean to create repo"), 
    generate: bool = typer.Option(False, "--generate", "-g" , help="Generates a Terraform Block Configuration"),
    out: bool = typer.Option(False, "--out" , "-o" , help="JSON Output of Workspace payload"),
    private: bool = typer.Option(True, "--private/--public" , help="Sets Repo Visibility"),
    terraform_version: str = typer.Option("1.1.3", "--tfversion" , "-v", help="Sets Terraform Version in Workspace")
    ):
    """
    Create Terraform Cloud VCS Workspace.
    
    User can create a repo or connect an existing repo.

    *Optional* - Repo creation requires a Github or Gitlab Account Configured.
    """ 
    if name == None:
        name = str(typer.prompt("Enter a Name of the workspace"))
    else:
        pass
    create_repo = typer.prompt("Create a new VCS Repo for this workspace? [Y/n]")
    private_repo = True if private == True else False #Sets the Private argument inside of the createRepoObject
    if create_repo == "y":
        repo_name = str(typer.prompt("Enter Name for New Repo"))
        repo_url = functions.createRepoObject(repo_name , private_repo)# creates repo and returns url
        repo_url_formatted = typer.style(repo_url, fg=typer.colors.GREEN)
        typer.echo(f"Created Github Repo: {repo_url_formatted}")
    else: 
        account = str(typer.prompt("Enter name of account or organization"))
        repo = str(typer.prompt("Enter the name of the Repo you want to use"))
        repo_url = "f{account}/{repo}"
        typer.echo(repo_url)
    payload = functions.createVcsWorkspace(name, terraform_version, repo_url)
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