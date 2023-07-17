import requests
import json

# Global Variables
OWNER = "ORGANIZATION-NAME-HERE"
TOKEN = "TOKEN-HERE"

# Request Header
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}

# To get repositories in the organization
def get_organization_repositories(headers=HEADERS):
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

# To check if master/develop is available
def check_repo_branch_availability(repository, branch):
    url = f"https://api.github.com/repos/{OWNER}/{repository}/branches/{branch}"
    response = requests.get(url, headers=HEADERS)
    if(response.status_code == 200):
        return True
    else:
        return False

# To update the branch protection
def update_branch_protection(repository):
    print(f"update_branch_protection {repository}")
    data = {
	"required_status_checks": {
		"strict": True,
		"contexts": []
	},
	"enforce_admins": True,
	"required_pull_request_reviews": {
		"dismissal_restrictions": {
			"users": [],
			"teams": []
		},
		"dismiss_stale_reviews": True,
		"require_code_owner_reviews": True,
		"required_approving_review_count": 2,
		"require_last_push_approval": True,
		"bypass_pull_request_allowances": {
			"users": [],
			"teams": []
		}
	},
	"restrictions": {
		"users": [],
		"teams": [],
		"apps": []
	},
	"required_linear_history": True,
	"allow_force_pushes": False,
	"allow_deletions": False,
	"block_creations": True,
	"required_conversation_resolution": True,
	"lock_branch": True,
	"allow_fork_syncing": True
}

    if(check_repo_branch_availability(repository, 'master')):
        url = f"https://api.github.com/repos/{OWNER}/{repository}/branches/master/protection"
        response = requests.put(url, headers=HEADERS, data=json.dumps(data))
        print(f"{repository}: Status Code {response.status_code}")
    else:
        print(f"{repository} : MASTER_BRANCH_NOT_AVAILABLE")
    
    if(check_repo_branch_availability(repository,'develop')):
        url = f"https://api.github.com/repos/{OWNER}/{repository}/branches/develop/protection"
        response = requests.put(url, headers=HEADERS, data=json.dumps(data))
        print(f"{repository}: Status Code {response.status_code}")
    else:
        print(f"{repository} : DEVELOP_BRANCH_NOT_AVAILABLE")


repositories = get_organization_repositories()
for repository in repositories:
    update_branch_protection(repository)
