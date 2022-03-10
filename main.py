import time
import os
import functions
import functions


TFC_ORGANIZATION = "devhop"
TC_MODE = os.getenv("TC_MODE", None)


def main ():
    dev_mode_enabled = False

    while TC_MODE == "Dev" or "DEV":
        dev_mode_enabled = True
        print(f"{functions.bcolors.BOLD}{functions.bcolors.WARNING}Development Mode{functions.bcolors.ENDC}")
        time.sleep(1)
        break

    new_build = str.lower(input(f"Do you want to create a new {functions.bcolors.HEADER}Terraform Workspace{functions.bcolors.ENDC}? (Y/n): "))
    workflow = str.lower(input(f"What type of {functions.bcolors.HEADER}Terraform Workspace{functions.bcolors.ENDC} is this? CLI or {functions.bcolors.BOLD}{functions.bcolors.OKCYAN}VCS{functions.bcolors.ENDC}: "))

    if new_build == "y" and workflow == "vcs":
        name = str(input("Enter a Name of the workspace: "))
        create_repo = input("Create a new VCS Repo for this workspace? (y/n): ")
        if create_repo == "y":
            repo_name = str(input("Enter Name for New Repo: "))
            repo_url = functions.createRepoObject(repo_name) # creates repo and returns url
            functions.createVcsWorkspace(name, "1.1.3", repo_url)
            ws_id = functions.getWsId(name)
            print(f"Workspace ID: {functions.bcolors.OKGREEN}{ws_id}{functions.bcolors.ENDC}")
            time.sleep(1)

            terraformBlockConfiguration = str(input("Do you want to update a Local Terraform Configuration with the new workspace? (y/n): "))
            tfVersion = functions.terraformVersion()

            if terraformBlockConfiguration == "y":
                    # The cloud meta block wasn't implemented until v1.1.0
                    if tfVersion >= 1.1:
                        functions.createTerraformBlock(workflow, name, TFC_ORGANIZATION) 
                    else:
                        print(f"{functions.bcolors.WARNING}Your Terraform Version cannot support the Cloud meta block. Upgrade to v1.1 or newer!{functions.bcolors.ENDC}")
            else:
                pass
            

            if dev_mode_enabled == True:   
                delete = input(f"Do you want to delete the last Workspace? (y/n) ")
                if delete == "y":
                    print(f"Deleting Workspace[{functions.bcolors.BOLD}{functions.bcolors.FAIL}{name}{functions.bcolors.ENDC}:{functions.bcolors.FAIL}{ws_id}{functions.bcolors.ENDC}]")
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
        print(f"Workspace ID: {functions.bcolors.OKGREEN}{ws_id}{functions.bcolors.ENDC}")
        time.sleep(1)


        terraformBlockConfiguration = str(input("Do you want to update a Local Terraform Configuration with the new workspace? (y/n): "))
        tfVersion = functions.terraformVersion()
        
        if terraformBlockConfiguration == "y":
            functions.createTerraformBlock("cli", name, TFC_ORGANIZATION)
        else:
            time.sleep(1)
            functions.clearConsole()


        if dev_mode_enabled == True:
            delete = input(f"Do you want to delete the last Workspace? (y/n) ")
            if delete == "y":
                print(f"Deleting Workspace[{functions.bcolors.BOLD}{functions.bcolors.FAIL}{name}{functions.bcolors.ENDC}:{functions.bcolors.FAIL}{ws_id}{functions.bcolors.ENDC}]")
                functions.deleteWorkspaces(name)
                cwd = str(os.getcwd)
                os.remove("payload.json") if os.path.exists("payload.json") else print("File Not Found!")
                os.remove("rendered_main.tf") if os.path.exists("rendered_main.tf") else print("File Not Found")
            else:
                print(f"{str.title(name)} workspace built in {TFC_ORGANIZATION}!")
        else:
            pass     
    else:
        functions.clearConsole()
    
    functions.banner()
    list_workspaces = str.lower(input(f"List all {functions.bcolors.HEADER}Terraform Workspaces{functions.bcolors.ENDC} in Terraform Cloud Organization: {functions.bcolors.OKBLUE}{functions.bcolors.BOLD}{TFC_ORGANIZATION}{functions.bcolors.ENDC}? (Y/n): "))

    if list_workspaces == "y":
        functions.listWorkspaces()
    else:
        functions.clearConsole()

    functions.banner()
    delete_workspaces = str.lower(input(f"Do you want to {functions.bcolors.FAIL}delete{functions.bcolors.ENDC} any {functions.bcolors.HEADER}Terraform Workspaces{functions.bcolors.ENDC} in Terraform Cloud Organization: {functions.bcolors.OKBLUE}{functions.bcolors.BOLD}{TFC_ORGANIZATION}{functions.bcolors.ENDC}? (Y/n): "))

    if delete_workspaces == "y":
        functions.listWorkspaces()
        ws_name = str.lower(input("Enter the name of Workspace(s): ")).split()
        for name in ws_name:
            try:
                functions.deleteWorkspaces(name)
            except:
                print(f"\n{functions.bcolors.WARNING}{name}{functions.bcolors.ENDC} not found in active Workspaces.")
            finally:
                functions.listWorkspaces()
    else:
        pass

if __name__ == '__main__':
 main()

