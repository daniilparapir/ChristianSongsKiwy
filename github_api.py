import requests

def get_latest_release(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        latest_release = response.json()
        return latest_release["tag_name"]
    else:
        raise Exception(f"Ошибка GitHub API: {response.status_code}")
