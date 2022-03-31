import re
from github import Github
import os

g = Github(os.getenv("GIT_TOKEN", None))


def createRepo(repo_name , repo_visabilty):
    x = g.get_user().create_repo(name=repo_name, auto_init=True, private=repo_visabilty)
    return x.id # returns the id of the new repo


def repoURL(id):
    x = g.get_repo(full_name_or_id=id)
    y = x.full_name # returns the owner/repo (User/Repo)
    return y

def createRepoObject(repo_name , repo_visabilty):
    try:
        x = createRepo(repo_name, repo_visabilty)
        url = repoURL(x)
        return url
    except g.GithubException.BadCredentialsException as creds:
        print("Bad Credentials. Check API Key Permissions")


def deleteRepo(repo_name):
    g.get_repo(full_name_or_id=repo_name).delete()
    print("Deletion Complete")

def listAllRepo():
    for repo in g.get_user().get_repos():
        print(repo.name)


def getUserName():
    user = g.get_user().login
    return user

