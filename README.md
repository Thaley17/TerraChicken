# TerraChicken (Terra🐓)

TO-DO: Add TC backstory

## Prerequisites 
1. `Python 3.6+`
2. Terraform Cloud Account [Here](https://app.terraform.io/signup/account) - Free Account Works
3. Github Account 

## Installation

To install Terra🐓 you can pull the package down for PyPi with the pip using the command below 
**Note** Terra🐓 uses libraries that have a hard dependency on `Python 3.6+`. You will need to have that version or newer

`pip install terrachicken` 

### Configuration 

TerraChicken can be initially configured two ways.

1. `Environment Variables` (Preferred)
2. `terrachicken --init` command allows you to add your tokens. **Note** If you are using an Env Var labeled `TFC_TOKEN` , `TFC_URL` or `GIT_TOKEN`. Those ENV Vars will take priority

### Environment Variables

- `TFC_TOKEN` - API Token generated from Terraform Cloud Settings. (help)
- `TFC_URL` - Terraform Cloud URL (app.terraform.io) unless using Terraform Enterprise
- `GIT_TOKEN` - Github Developer Access Token (Repo CRUD Perms at minimum)

To set an environment token use the following `export TFC_URL='app.terraform.io'`





