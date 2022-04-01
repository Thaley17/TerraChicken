# TerraChicken (Terra🐓)

Terrachicken is a `cli` tool for interacting with Terraform Cloud Workspaces. Terra🐓 allows users to create, list, and delete TFC Workspaces. Terra🐓 supports configuring VCS backed workspaces for Github and Gitlab (Future Version). Terra🐓 was developed to help solve the 🐓 and 🥚 problem with Terraform Cloud automation. Allowing developers and practitioners an easy way to create and destroy workspaces from the command line. Terra🐓 even generates `Terraform Backend` configurations. *This project was created to help solve problems but more so to learn Python and CLI development*

## Prerequisites 
1. `Python 3.6+`
2. Terraform Cloud Account [Here](https://app.terraform.io/signup/account) - Free Account Works
3. Github Account 

## Installation

To install Terra🐓 you can pull the package down for PyPi with the pip using the command below 
**Note** Terra🐓 uses libraries that have a hard dependency on `Python 3.6+`. You will need to have that version or newer

`pip install terrachicken` 

## Configuration 

TerraChicken only supports Environment Variables currently. Future versions will have built in functionality to support initial configuration.

1. `Environment Variables` 


### Environment Variables

- `TFC_TOKEN` - API Token generated from Terraform Cloud Settings. 
- `TFC_URL` - Terraform Cloud URL (app.terraform.io) unless using Terraform Enterprise
- `TFC_ORG` - Terraform Cloud Organiztion Name
- `GIT_TOKEN` - Github Developer Access Token (Repo CRUD Perms at minimum)

To set an environment token use the following `export TFC_URL='app.terraform.io'`


Hint: *After you set your tokens. You can install the built in `auto completion` with the `terrachicken --install-completion` command.*

## Using Terra🐓

Terrachicken support cli `--help` options with all commands.

## Creating Workspaces

Terra🐓 supports creating `Local` and `VCS` or Version Control System (Github/Gitlab) workspaces. 

### Local Workspaces
Example:

`terrachicken create workspace local` 

You will be prompted to enter a `name` for your workspace. After a successful completion your new Workspace ID will be printed to the terminal.

![tc local workspace](https://github.com/Thaley17/TerraChicken/blob/media/local_wksp.png?raw=true)


### VCS Workspace

`terrachicken create workspace vcs`

**Note: The Github OAuth provider must be configured in Terraform Cloud prior to building VCS workspaces.**

Creating a VCS backed workspace requires you to either create a repo or link and existing repo to the workspace. The default is to create a Github Repo along side the workspace. 

![tc vcs workspace](https://github.com/Thaley17/TerraChicken/blob/media/vcs_w.png?raw=true)

#### Create Workspace VCS Options

- `--name`: Name of Workspace
- `--generate`: Generate Terraform Block Configuration
- `--out`: Exports TFC Configuration via `payload.json` 
- `--tfversion`: Set Terraform Version in Workspace
- `--create_repo`: Create Repo or nah
- `--private`: Set Github Repo to Private
- `--public`: Set Github Repo to Public
  
### Generating Terraform Block Configurations
Example:

`terrachicken create workspace vcs --name TerrachickenTest1 --generate`

Example `rendered_main.tf`:

```hcl
terraform {
  cloud { 
    organization = "aBakersDozen"

    workspaces {
      name = "TerrachickenTest1"
    }
  }
}
```

Both `create workspace local` and `create workspace vcs` support generating a Terraform Block configuration to be implemented inside of your Terraform code. To read more about the Terraform Block Syntax click [here](https://www.terraform.io/language/settings). Using the `--generate` or `-g` option at the end of the command will output a `rendered_main.tf` file to your current working directory. 

The Terraform Block settings will differ based on your workspace type. If you are creating a `local` workspace. The configuration sets `backend` with your workspace name. If you are creating a `vcs` workspace the configuration sets the `cloud` block. To use the VCS generated main.tf file, you will need to run the `terraform login` command if you want to execute cli commands for terraform. Click [here](https://www.terraform.io/cli/cloud/settings) to read about `cloud block` and `terraform login`.

### List

Terra🐓 lets you list your current TFC Workspaces and Repositories with a two simple commands.

`terrachicken list workspaces` or `terrachicken list repos`

### Delete

#### Workspaces

You can delete workspaces from your accounts with the `terrachicken delete workspace` command. Terra🐓 will list the available workspaces to delete. You will be prompted to enter the workspace name you want to delete. You can enter a single name or multiple workspaces by adding them as such `wksp1 wksp2 wksp3`. After every workspace deletion a new list of current workspaces will be printed.

#### Repos

You can delete repos from your github account with the `terrachicken delete repos` command. Terra🐓 will list all available repos to delete. You will be prompted to enter the name of the repo you want to delete. 

Deleting repos will also prompt a confirmation of deletion for the account/repo you want to delete. *Note: Once you delete an account Terrachicken can not restore that repo*


## TO-DO

- [ ] TO-DO: Add pytest
- [ ] TO-DO: Add init configurations to set default OAuth Client
- [ ] TO-DO: Add --repo flag to copy --name flag
- [ ] TO-DO: Add Gitlab VCS Options
- [ ] TO-DO: Remove the utils.bcolors class, sub for the rich library
- [ ] TO-DO: Add option to delete workspace and repo at same time.
- [ ] TO-DO: Add more options to the TF Workspace Configuration.
