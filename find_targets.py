import requests
import atexit
import re

GITHUB_USER = "mac-chaffee"
GITHUB_PAT = ""

missing_urls = []
missing_python_size = []
found_urls = []

def print_findings():
    print(f"{missing_urls=}")
    print(f"{missing_python_size=}")
    print("Here is the list of 'tiny' Python packages:")
    print(f"{found_urls=}")

def find_github_url(package_name, project_urls, description):
    github_regex = r'(https?://github.com/[a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_]+)'
    potential_url = ""
    for _, v in project_urls.items():
        if re.search(github_regex, v):
            potential_url = v
            break
    # Try to scrape the description
    if not potential_url and description:
        matches = re.findall(github_regex, description)
        matches = [m for m in matches if package_name in m]
        if matches:
            potential_url = matches[0]

    if potential_url.endswith('.git'):
        potential_url = potential_url[:-4]
    return potential_url

def main():
    with open('top_package_list.txt', 'r') as f:
        packages = f.read().split()

    for package in packages:
        package_url = f"https://pypi.org/pypi/{package}/json"
        response = requests.get(package_url)
        if not response.ok or not response.json():
            print(f"error fetching {package}: {response.text} skipping")
            continue
        project_urls = response.json()['info'].get('project_urls')
        if not project_urls:
            project_urls = {}
        homepage = response.json()['info'].get('home_page')
        if homepage:
            project_urls['__homepage'] = homepage
        repo_url = find_github_url(package, project_urls, response.json()['info'].get('description'))
        if not repo_url:
            missing_urls.append(package_url)
            continue

        repo_owner, repo_name = repo_url.split('/')[3:5]
        assert repo_owner and repo_name

        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/languages"

        response = requests.get(api_url, auth=(GITHUB_USER, GITHUB_PAT))
        if not response.ok:
            print(f"error fetching {package}: {response.text} skipping")
        lang_sizes = response.json()
        python_size = lang_sizes.get('Python', 0)
        if not python_size:
            missing_python_size.append(package_url)
            continue

        # Is this a tiny library?
        if python_size < 3000 and 'C' not in lang_sizes and 'C++' not in lang_sizes:
            print(f"****TARGET SIGHTED: {repo_url} only has {python_size} python bytes and no C/C++ code")
            found_urls.append({'name': package, 'repo_url': repo_url, 'package_url': package_url, 'size': python_size})
        print(f"skipping https://pypi.org/pypi/{package}/json, it's {python_size} bytes")


if __name__ == '__main__':
    atexit.register(print_findings)
    main()
