from hackdayproject.repo.models import Commit
from django.conf import settings as conf
from django.utils import timezone
import requests

now = timezone.now()


def get_user_data(username):
    '''Github 사용자 정보 반환

    Args:
        username : Github으로 로그인한 사용자 이름

    Returns:
        값을 가져오는데 성공했을 경우 Dict
        값을 가져오는데 실패했을 경우 Str
    '''
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
    '''Github 사용자의 조직 정보 반환

    Args:
        username : Github으로 로그인한 사용자 이름

    Returns:
        값을 가져오는데 성공했을 경우 Dict in List
        값을 가져오는데 실패했을 경우 Str
    '''
    try:
        orgs_data = requests.get(
            conf.GIT_API_URL + "/users/" + username + "/orgs" + conf.SUFFIX
        )
        header_link = orgs_data.headers
        orgs_data = orgs_data.json()

        orgs_data = [
            {
                "orgs_name": orgs["login"],
                "avatar_url": orgs["avatar_url"]
            } for orgs in orgs_data]

        if 'Link' in header_link.keys():
            header_link = header_link["Link"]

            while 'rel="next"' in header_link:
                next_link = header_link.split('rel="next"')[0]
                next_link = next_link[1:len(next_link) - 3]

                next_orgs_data = requests.get(next_link)
                header_link = next_orgs_data.headers["Link"]
                next_orgs_data = next_orgs_data.json()
                orgs_data += [
                    {
                        "orgs_name": orgs["login"],
                        "avatar_url": orgs["avatar_url"]
                    } for orgs in next_orgs_data]
    except Exception as e:
        print(e)
        orgs_data = "Can't get user organization data."

    return orgs_data


def get_orgs_repo(orgs_name):
    '''Github 조직 레파지토리 정보 반환

    Args:
        orgs_name : Github 조직 이름

    Returns:
        값을 가져오는데 성공했을 경우 Dict in List
        값을 가져오는데 실패했을 경우 Str
    '''
    try:
        now = timezone.now()
        orgs_repo_data = requests.get(
            conf.GIT_API_URL + "/orgs/" + orgs_name + "/repos" + conf.SUFFIX
        )
        header_link = orgs_repo_data.headers
        orgs_repo_data = orgs_repo_data.json()

        orgs_repo_data = [
            {
                "full_name": repo["full_name"],
                "owner": repo["owner"]["login"],
                "language": repo["language"],
                "description": repo["description"],
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "pushed_at": repo["pushed_at"]
            } for repo in orgs_repo_data]

        if 'Link' in header_link.keys():
            header_link = header_link["Link"]

            while 'rel="next"' in header_link:
                next_link = header_link.split('rel="next"')[0]
                next_link = next_link[1:len(next_link) - 3]

                next_orgs_repo_data = requests.get(next_link)
                header_link = next_orgs_repo_data.headers["Link"]
                next_orgs_repo_data = next_orgs_repo_data.json()
                orgs_repo_data += [
                    {
                        "full_name": repo["full_name"],
                        "owner": repo["owner"]["login"],
                        "language": repo["language"],
                        "description": repo["description"],
                        "created_at": repo["created_at"],
                        "updated_at": repo["updated_at"],
                        "pushed_at": repo["pushed_at"]
                    } for repo in next_orgs_repo_data]
    except Exception as e:
        print(e)
        orgs_repo_data = "Can't get user organization data."

    return orgs_repo_data


def get_user_repo(username):
    '''Github 사용자 레파지토리 정보 반환

    Args:
        username : Github으로 로그인한 사용자 이름

    Returns:
        값을 가져오는데 성공했을 경우 Dict in List
        값을 가져오는데 실패했을 경우 Str
    '''
    try:
        user_repo = requests.get(
            conf.GIT_API_URL + '/users/' + username + '/repos',
            params={
                "type": "all",
                "sort": "updated",
                "client_id": conf.SOCIAL_AUTH_GITHUB_KEY,
                "client_secret": conf.SOCIAL_AUTH_GITHUB_SECRET
            }
        )
        header_link = user_repo.headers
        user_repo = user_repo.json()
        user_repo = [
            {
                "full_name": repos["full_name"],
                "owner": repos["owner"]["login"],
                "language": repos["language"],
                "description": repos["description"],
                "created_at": repos["created_at"],
                "updated_at": repos["updated_at"],
                "pushed_at": repos["pushed_at"]
            } for repos in user_repo]

        if 'Link' in header_link.keys():
            header_link = header_link["Link"]

            while 'rel="next"' in header_link:
                # Get next page link using split and slicing
                next_link = header_link.split('rel="next"')[0]
                next_link = next_link[1:len(next_link) - 3]

                # Request user repos using next_link
                next_user_repo = requests.get(next_link)
                # Get headers Link data
                header_link = next_user_repo.headers["Link"]
                # Response data convert to dict
                next_user_repo = next_user_repo.json()
                # Append user_repo data
                user_repo += [
                    {
                        "full_name": repos["full_name"],
                        "owner": repos["owner"]["login"],
                        "language": repos["language"],
                        "description": repos["description"],
                        "created_at": repos["created_at"],
                        "updated_at": repos["updated_at"],
                        "pushed_at": repos["pushed_at"]
                    } for repos in next_user_repo]

    except Exception as e:
        print(e)
        user_repo = "Can't get user repository data."

    return user_repo


def get_repo_commit(username, repo_full_name, check_modified=True):
    '''수정된 Github 레파지토리 커밋 정보 반환

    Args:
        repo_full_name : user/repo 형식의 Str
        check_modified : 오늘 기준 수정 여부 확인 Boolean

    Returns:
        값을 가져오는데 성공했을 경우 Dict in List
        값을 가져오는데 실패했을 경우 Str
    '''
    try:
        headers = {}

        if check_modified:
            headers = {
                "If-Modified-Since": now.strftime('%a, %d %b %Y 00:00:00 GMT')
            }

        user_repo_commit = requests.get(
            conf.GIT_API_URL + "/repos/" + repo_full_name + "/commits",
            params={
                "client_id": conf.SOCIAL_AUTH_GITHUB_KEY,
                "client_secret": conf.SOCIAL_AUTH_GITHUB_SECRET,
                'author': username
            },
            headers=headers
        )

        header_link = user_repo_commit.headers
        status_code = user_repo_commit.status_code

        print(header_link)
        print(status_code)

        if status_code == 304:
            return "No Updated Repository."

        if status_code == 409:
            return "Empty Repository."

        user_repo_commit = user_repo_commit.json()
        user_repo_commit = [
            {
                "sha": c["sha"],
                "email": c["commit"]["committer"]["email"],
                "date": c["commit"]["committer"]["date"]
            } for c in user_repo_commit]

        if 'Link' in header_link.keys():
            header_link = header_link["Link"]

            while 'rel="next"' in header_link:
                next_link = header_link.split('rel="next"')[0]
                next_link = next_link[1:len(next_link) - 3]

                next_user_repo_commit = requests.get(next_link)
                header_link = next_user_repo_commit.headers["Link"]
                next_user_repo_commit = next_user_repo_commit.json()
                user_repo_commit += [
                    {
                        "sha": c["sha"],
                        "email": c["commit"]["committer"]["email"],
                        "date": c["commit"]["committer"]["date"]
                    } for c in next_user_repo_commit]
    except Exception as e:
        print(e)
        user_repo_commit = "Can't get " + repo_full_name + " commits"

    return user_repo_commit


def update_user_commit(username, repo, checked_modified):
    commits = get_repo_commit(
        username,
        repo.full_name,
        check_modified=checked_modified
    )

    if not type(commits) is str:
        for commit in commits:
            new_commit = Commit(
                repository=repo,
                sha=commit["sha"],
                email=commit["email"],
                date=commit["date"]
            )
            new_commit.save()
