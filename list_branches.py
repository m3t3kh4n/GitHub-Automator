# Author: Hajiahmad Ahmadzada
# Description: This script gets the list of branches in the given repository.
# Version: 1.0
# Date: 2023-06-06

import requests

# Edit this values
OWNER = "YOUR-ORGANIZATION"
TOKEN = "YOUR-TOKEN"
repository = "REPOSITORY-NAME"

# Required Header values
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}

def list_branches(repository):
    branches = []
    page_number = 1
    while True:
        url = f"https://api.github.com/repos/{OWNER}/{repository}/branches?per_page=100&page={page_number}"
        response = requests.get(url, headers=headers)
        if(response.json() == []):
            break
        for branch in response.json():
            branches.append(branch["name"])
        page_number+=1
    return branches
