
import os
import json
import re
import utils
from terrasnek.api import TFC
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

TFC_TOKEN = os.getenv("TFC_TOKEN", None)
TFC_URL = os.getenv("TFC_URL", None)
TFC_ORGANIZATION = "devhop"

api = TFC(TFC_TOKEN, url=TFC_URL)
api.set_org(TFC_ORGANIZATION)


env = Environment(
    loader= FileSystemLoader("templates"),
    autoescape= select_autoescape()
    )

def getWsId(ws_name):
        #using the search selector
        ws = api.workspaces.list(search=ws_name)
        ws_id = ws["data"][0]["id"] #since workspace names have to be unique the result will only have element
        return ws_id

# Creates Workspaces with VCS Repo. Used to store state only
def createLocalWorkspace(ws_name):
    create_payload = {'data': {'type': "workspaces" , 'attributes': {'name': ws_name , 'execution-mode': 'local' }}}
    api.workspaces.create(create_payload)
    print("Creation Completed!")
    return create_payload

# Creates VCS Workspace, Repo must be created first. Check the github functions for the CreateRepoObject()
def createVcsWorkspace(ws_name, tf_version, repo_url):
    oauth_client = api.oauth_clients.list() # need to retrieve a list of oauth clients IOT get oauth token id
    token_list = {}
    for i in oauth_client['data']: #Looping through data to add all OAUTH clients to a dict so user can pick the oauth client
        display_name = i['attributes']['service-provider']
        oauth_token = i['relationships']['oauth-tokens']['data'][0]['id']
        token_format = {display_name: {'token': oauth_token}}
        token_list.update(token_format)
    keys = token_list.keys() # selects keys from the dict above to present to user
    print(keys)
    oauth_selection = input("Select Client from above: " )
    id = token_list.get(oauth_selection)
    oauth_token_id = id['token'] #grabs oauth_token from the oauth client in the dict for the create_payload object
    create_payload = {'data': {'type': "workspaces" , 'attributes': {'name': ws_name , 'execution-mode': 'remote' , 
    'source-name': 'Created with TerraChicken', 'terraform-version': tf_version , 'working-directory': "", 'vcs-repo': {'identifier': repo_url , 'oauth-token-id': oauth_token_id} }}}
    api.workspaces.create(create_payload)
    print("Creation Completed!")
    return create_payload


def createTerraformBlock(workflow, name, org):
    mainTemplate = env.get_template("terraform_block.jinja2") #using j2 to generate template based on the workflow variable
    with open("rendered_main.tf" , "w") as f:
       f.write(mainTemplate.render(workflow_type=workflow , ws_name=name , ws_org=org))
    cwd = os.getcwd
    path = f"File: 'rendered_main.tf' can be found at {cwd}!"
    print(path)

def terraformVersion():
    output = os.popen("terraform --version").read()
    regex = r"[a-zA-Z]\d{1,2}\.\d{1,2}\.\d{1,3}"
    matches = re.finditer(regex, output, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        x = "{match}".format(match = match.group()).replace("v", "").split(sep= ".")
        version = float(x[0] + "." + x[1])
    return version

def listWorkspaces():
    workspaces = api.workspaces.list_all()
    reply_data = workspaces["data"]
    for elem in reply_data:
        ws_id = elem["id"]
        ws_name = elem["attributes"]["name"]
        print(f"{ws_id}:{utils.bcolors.BOLD}{utils.bcolors.HEADER}{ws_name}{utils.bcolors.ENDC}")

def deleteWorkspaces(*args):
    def convertTuple(tup):
        str = ""
        for item in tup:
            str = str + item
            return str
    name = convertTuple(args)
    api.workspaces.destroy(workspace_name=name)

