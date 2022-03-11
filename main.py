import time
import os
import functions
import utils


TFC_ORGANIZATION = "devhop"
TC_MODE = os.getenv("TC_MODE", None)


def main ():
    dev_mode_enabled = False

    while TC_MODE == "Dev" or "DEV":
        dev_mode_enabled = True
        print(f"{utils.bcolors.BOLD}{utils.bcolors.WARNING}Development Mode{utils.bcolors.ENDC}")
        time.sleep(1)
        break

    new_build = str.lower(input(f"Do you want to create a new {utils.bcolors.HEADER}Terraform Workspace{utils.bcolors.ENDC}? (Y/n): "))
    workflow = str.lower(input(f"What type of {utils.bcolors.HEADER}Terraform Workspace{utils.bcolors.ENDC} is this? CLI or {utils.bcolors.BOLD}{utils.bcolors.OKCYAN}VCS{utils.bcolors.ENDC}: "))

    if new_build == "y" and workflow == "vcs":
        name = str(input("Enter a Name of the workspace: "))
        create_repo = input("Create a new VCS Repo for this workspace? (y/n): ")
        if create_repo == "y":
            repo_name = str(input("Enter Name for New Repo: "))
            repo_url = functions.createRepoObject(repo_name) # creates repo and returns url
            functions.createVcsWorkspace(name, "1.1.3", repo_url)
            ws_id = functions.getWsId(name)
            print(f"Workspace ID: {utils.bcolors.OKGREEN}{ws_id}{utils.bcolors.ENDC}")
            time.sleep(1)

            terraformBlockConfiguration = str(input("Do you want to update a Local Terraform Configuration with the new workspace? (y/n): "))
            tfVersion = functions.terraformVersion()

            if terraformBlockConfiguration == "y":
                    # The cloud meta block wasn't implemented until v1.1.0
                    if tfVersion >= 1.1:
                        functions.createTerraformBlock(workflow, name, TFC_ORGANIZATION) 
                    else:
                        print(f"{utils.bcolors.WARNING}Your Terraform Version cannot support the Cloud meta block. Upgrade to v1.1 or newer!{utils.bcolors.ENDC}")
            else:
                pass
            

            if dev_mode_enabled == True:   
                delete = input(f"Do you want to delete the last Workspace? (y/n) ")
                if delete == "y":
                    print(f"Deleting Workspace[{utils.bcolorsBOLD}{utils.bcolorsFAIL}{name}{utils.bcolorsENDC}:{utils.bcolors.FAIL}{ws_id}{utils.bcolors.ENDC}]")
                    functions.deleteWorkspaces(name)
                    x = f"Thaley17/{name}"
                    functions.deleteRepo(x)
                    cwd = str(os.getcwd)
                    os.remove("payload.json") if os.path.exists("payload.json") else print("File Not Found!")
                    os.remove("rendered_main.tf") if os.path.exists("rendered_main.tf") else print("File Not Found")
                else:
                    print(f"{str.title(name)} workspace built in {TFC_ORGANIZATION}!")
        else:
            pass

    elif new_build == "y":
        name = str(input("Enter a Name of the workspace: "))
        functions.createLocalWorkspace(name)
        ws_id = functions.getWsId(name)
        print(f"Workspace ID: {utils.bcolors.OKGREEN}{ws_id}{utils.bcolors.ENDC}")
        time.sleep(1)


        terraformBlockConfiguration = str(input("Do you want to update a Local Terraform Configuration with the new workspace? (y/n): "))
        tfVersion = functions.terraformVersion()
        
        if terraformBlockConfiguration == "y":
            functions.createTerraformBlock("cli", name, TFC_ORGANIZATION)
        else:
            time.sleep(1)
            utils.clearConsole()


        if dev_mode_enabled == True:
            delete = input(f"Do you want to delete the last Workspace? (y/n) ")
            if delete == "y":
                print(f"Deleting Workspace[{utils.bcolors.BOLD}{utils.bcolors.FAIL}{name}{utils.bcolors.ENDC}:{utils.bcolors.FAIL}{ws_id}{utils.bcolors.ENDC}]")
                functions.deleteWorkspaces(name)
                cwd = str(os.getcwd)
                os.remove("payload.json") if os.path.exists("payload.json") else print("File Not Found!")
                os.remove("rendered_main.tf") if os.path.exists("rendered_main.tf") else print("File Not Found")
            else:
                print(f"{str.title(name)} workspace built in {TFC_ORGANIZATION}!")
        else:
            pass     
    else:
        utils.clearConsole()
    
    utils.banner()
    list_workspaces = str.lower(input(f"List all {utils.bcolors.HEADER}Terraform Workspaces{utils.bcolors.ENDC} in Terraform Cloud Organization: {utils.bcolors.OKBLUE}{utils.bcolors.BOLD}{TFC_ORGANIZATION}{utils.bcolors.ENDC}? (Y/n): "))

    if list_workspaces == "y":
        functions.listWorkspaces()
    else:
        utils.clearConsole()

    utils.banner()
    delete_workspaces = str.lower(input(f"Do you want to {utils.bcolors.FAIL}delete{utils.bcolors.ENDC} any {utils.bcolors.HEADER}Terraform Workspaces{utils.bcolors.ENDC} in Terraform Cloud Organization: {utils.bcolors.OKBLUE}{utils.bcolors.BOLD}{TFC_ORGANIZATION}{utils.bcolors.ENDC}? (Y/n): "))

    if delete_workspaces == "y":
        functions.listWorkspaces()
        ws_name = str.lower(input("Enter the name of Workspace(s): ")).split()
        for name in ws_name:
            try:
                functions.deleteWorkspaces(name)
            except:
                print(f"\n{utils.bcolors.WARNING}{name}{utils.bcolors.ENDC} not found in active Workspaces.")
            finally:
                functions.listWorkspaces()
    else:
        pass

if __name__ == '__main__':
 main()

