from hackdayproject.utils.github_api \
    import get_user_repo, get_orgs_repo
from datetime import datetime
from django.utils import timezone
from collections import OrderedDict
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


def calculate_current_streak(repos):
    commit_logs, current_streak = {}, 0
    for repo in repos:
        commits = repo.commit_set.all()

        for commit in commits:
            date = str(convert_to_localtime(commit.date))[:10]

            if date in commit_logs.keys():
                commit_logs[date] += 1

            else:
                commit_logs[date] = 1

    commit_logs = OrderedDict(
        sorted(commit_logs.items(), key=lambda t: t[0]))

    commit_logs = list(commit_logs.items())
    before_commit = string_date_to_datetime(commit_logs[0][0])

    for i in range(1, len(commit_logs)):
        now_commit = string_date_to_datetime(commit_logs[i][0])
        commit_day_diff = (now_commit - before_commit).days

        if commit_day_diff == 1:
            current_streak += 1
        else:
            current_streak = 0

        before_commit = now_commit

    return current_streak
