from hackdayproject.utils.github_api \
    import get_user_repo, get_orgs_repo
from datetime import datetime
from django.utils import timezone
import pytz


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


def string_date_to_datetime(date):
    return datetime.strptime(date, "%Y-%m-%d")


def convert_to_localtime(utctime):
    fmt = '%Y-%m-%d %H:%M:%S'
    utc = utctime.replace(tzinfo=pytz.UTC)
    local_timezone = utc.astimezone(timezone.get_current_timezone())
    return local_timezone.strftime(fmt)
