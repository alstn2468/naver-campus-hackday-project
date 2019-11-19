from django.conf import settings as conf
import requests


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
        ).json()

        orgs_data = [{"orgs_name": orgs["login"],
                      "avatar_url": orgs["avatar_url"]} for orgs in orgs_data]
    except Exception as e:
        print(e)
        orgs_data = "Can't get user organization data."

    return orgs_data


def get_orgs_repo(orgs_name):
    '''Github 조직 레파지토리 정보 반환

    Args:
        orgs_name : Github 조직 이름

    Returns:
        값을 가져오는데 성공했을 경우 List
        값을 가져오는데 실패했을 경우 Str
    '''
    try:
        orgs_repo_data = requests.get(
            conf.GIT_API_URL + "/orgs/" + orgs_name + "/repos" + conf.SUFFIX
        ).json()

        orgs_repo_data = [repo["full_name"] for repo in orgs_repo_data]
    except Exception as e:
        print(e)
        orgs_repo_data = "Can't get user organization data."

    return orgs_repo_data


def get_user_repo(username):
    '''Github 사용자 레파지토리 정보 반환

    Args:
        username : Github으로 로그인한 사용자 이름

    Returns:
        값을 가져오는데 성공했을 경우 List
        값을 가져오는데 실패했을 경우 Str
    '''
    try:
        user_repo = requests.get(
            conf.GIT_API_URL + '/users/' + username + '/repos' + conf.SUFFIX, {
                "type": "all",
                "sort": "updated"
            })
        header_link = user_repo.headers
        user_repo = user_repo.json()
        user_repo = [repos["full_name"] for repos in user_repo]

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
                user_repo += [repos["full_name"] for repos in next_user_repo]

    except Exception as e:
        print(e)
        user_repo = "Can't get user repository data."

    return user_repo


def get_user_repo_commit(repo_full_name):
    '''Github  레파지토리 커밋 정보 반환

    Args:
        repo_full_name : user/repo 형식의 Str

    Returns:
        값을 가져오는데 성공했을 경우 Dict in List
        값을 가져오는데 실패했을 경우 Str
    '''
    try:
        user_repo_commit = requests.get(
            conf.GIT_API_URL + "/repos/" + repo_full_name + "/commits" + conf.SUFFIX
        )
        # GET /repos/:user/:repo/:commits
        # alstn2468.github.io기준 450개 모두 가져와 지는 것을 확인
        header_link = user_repo_commit.headers
        user_repo_commit = user_repo_commit.json()
        user_repo_commit = [c["committer"] for c in user_repo_commit]

        if 'Link' in header_link.keys():
            header_link = header_link["Link"]

            while 'rel="next"' in header_link:
                next_link = header_link.split('rel="next"')[0]
                next_link = next_link[1:len(next_link) - 3]

                next_user_repo_commit = requests.get(next_link)
                header_link = next_user_repo_commit.headers["Link"]
                next_user_repo_commit = next_user_repo_commit.json()

                user_repo_commit += [c["committer"]
                                     for c in next_user_repo_commit]
    except Exception as e:
        print(e)
        user_repo_commit = "Can't get " + repo_full_name + " events"

    return user_repo_commit
