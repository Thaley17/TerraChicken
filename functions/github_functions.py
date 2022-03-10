import re
from github import Github
import os

g = Github(os.getenv("GIT_TOKEN", None))



# for repo in g.get_user().get_repos():
#     print(f"{repo.name}:{repo.id}:{repo.created_at}")


# g.get_user().create_repo(name="ayeok")


def createRepo(repo_name):
    x = g.get_user().create_repo(name=repo_name, auto_init=True)
    return x.id # returns the id of the new repo


def repoURL(id):
    x = g.get_repo(full_name_or_id=id)
    y = x.full_name # returns the owner/repo (User/Repo)
    return y

def createRepoObject(repo_name):
    x = createRepo(repo_name)
    url = repoURL(x)
    return url

def deleteRepo(repo_name):
    g.get_repo(full_name_or_id=repo_name).delete()
    print("Deletion Complete")

