import requests

def get_latest_release(token, username, repo):
    headers = {"Authorization": f"token {token}"}
    url = f"https://api.github.com/repos/{username}/{repo}/releases/latest"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка {response.status_code} при получении релиза")
