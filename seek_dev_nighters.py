import requests
from requests import HTTPError
from datetime import datetime
from pytz import timezone
from collections import defaultdict


def load_attempts(api_url):
    page = 1
    first_iteration = True
    while True:
        if first_iteration:
            first_iteration = False
        else:
            if page > pages_count:
                break
        params = {"page": page}
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
        except (ConnectionError, TimeoutError, HTTPError):
            yield None
        response_content = response.json()
        pages_count = response_content["number_of_pages"]
        page += 1
        for record in response_content["records"]:
            username = record["username"]
            timestamp = record["timestamp"]
            timezone = record["timezone"]
            yield {
                "username": username,
                "timestamp": timestamp,
                "timezone": timezone,
            }


def is_midnighter(user_dt):
    send_check_hour_from = 0
    send_check_hour_to = 4
    return (send_check_hour_from
            <= user_dt.hour
            <= send_check_hour_to)


def print_title(title_was_printed):
    if not title_was_printed:
        print("Midnighters on devman detected:\n")


def print_midnighter_activity(midnighter_activity):
    for username, user_dt in midnighter_activity.items():
        print("User {} sent the tasks for review at: \n{}\n".format(
            username,
            "\n".join(user_dt)
        ))


if __name__ == "__main__": 
    api_url = "https://devman.org/api/challenges/solution_attempts/"
    title_was_printed = False
    midnighters_activity = defaultdict(list)
    for attempt in load_attempts(api_url):
        if not attempt:
            exit("Site {} is unavailable!".format(api_url))
        user_timestamp = attempt["timestamp"]
        user_timezone = attempt["timezone"]
        username = attempt["username"]
        midnighter_dt = datetime.fromtimestamp(
            user_timestamp,
            timezone(user_timezone)
        )
        if is_midnighter(midnighter_dt):
            print_title(title_was_printed)
            title_was_printed = True
            midnighters_activity[username].append(str(
                midnighter_dt.replace(tzinfo=None))
            )
    print_midnighter_activity(midnighters_activity)
