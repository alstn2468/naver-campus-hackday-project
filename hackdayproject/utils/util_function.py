from hackdayproject.utils.github_api \
    import get_user_repo, get_user_orgs, get_orgs_repo


def get_user_all_repo(username, orgs_data):
    user_repo = get_user_repo(username)

    for orgs in orgs_data:
        orgs_repo_temp = get_orgs_repo(orgs["orgs_name"])
        if type(orgs_repo_temp) is list:
            while len(orgs_repo_temp) > 0:
                check = True

                for repo in user_repo:
                    if repo["full_name"] == orgs_repo_temp[0]["full_name"]:
                        orgs_repo_temp.pop(0)
                        check = False
                        break

                if check:
                    user_repo.append(orgs_repo_temp.pop(0))

    return user_repo
