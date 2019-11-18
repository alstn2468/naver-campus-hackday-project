from django.conf import settings as conf
import requests


def get_user_data(username):
    try:
        user_data = requests.get(
            conf.GIT_API_URL + "/users/" + username + conf.SUFFIX
        ).json()

        user_data = {
            "avatar_url": user_data["avatar_url"],
            "company": user_data["company"],
            "blog_url": user_data["blog"],
            "location": user_data["location"],
            "bio": user_data["bio"],
            "public_repos_count": user_data["public_repos"],
            "followers": user_data["followers"],
            "following": user_data["following"]
        }
    except Exception as e:
        print(e)
        user_data = "Can't get user data."

    return user_data


def get_user_orgs(username):
    try:
        orgs_data = requests.get(
            conf.GIT_API_URL + "/users/" + username + "/orgs" + conf.SUFFIX
        ).json()

        orgs_data = [orgs["login"] for orgs in orgs_data]
    except Exception as e:
        print(e)
        orgs_data = "Can't get user organization data."

    return orgs_data


def get_orgs_repos(orgs_name):
    try:
        orgs_repo_data = requests.get(
            conf.GIT_API_URL + "/orgs/" + orgs_name + "/repos" + conf.SUFFIX
        ).json()

        orgs_repo_data = [repo["full_name"] for repo in orgs_repo_data]
    except Exception as e:
        print(e)
        orgs_repo_data = "Can't get user organization data."

    return orgs_repo_data


def get_user_repos(username, repo_count):
    try:
        user_repo = requests.get(
            conf.GIT_API_URL + '/users/' + username + '/repos' + conf.SUFFIX
            + '&per_page=' + repo_count, {
                "type": "all",
                "sort": "updated"
            }).json()

        user_repo = [repos["full_name"] for repos in user_repo]
    except Exception as e:
        print(e)
        user_repo = "Can't get user repository data."

    return user_repo
