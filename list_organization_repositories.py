# Author: Hajiahmad Ahmadzada
# Description: This script gets the list of repositories which is in the given GitHub Organization.
# Version: 1.0
# Date: 2023-06-05

import requests

OWNER = "YOUR-ORGANIZATION"
TOKEN = "YOUR-TOKEN"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}

def list_organization_repositories(organization, headers=headers):
    repositories = []
    page_number = 1
    while True:
        url = f"https://api.github.com/orgs/{OWNER}/repos?state=active&per_page=100&page={page_number}"
        response = requests.get(url, headers=headers)
        if(response.json() == []):
            break
        for repository in response.json():
            repositories.append(repository["name"])
        page_number+=1
    return repositories
