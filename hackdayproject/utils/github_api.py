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


def get_user_repos(username, repo_count):
    try:
        user_repos = requests.get(
            conf.GIT_API_URL + '/users/' + username + '/repos' + conf.SUFFIX
            + '&per_page=' + repo_count, {
                "type": "all",
                "sort": "updated"
            }).json()

        user_repos = [repos["full_name"] for repos in user_repos]
    except Exception as e:
        print(e)
        user_repos = "Can't get user repository data."

    return user_repos
