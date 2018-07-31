import requests
import pytz
from datetime import datetime
from pytz import timezone


def load_attempts(page_number, api_url):
    for page in range(1, page_number+1):
        params = {"page": page}
        try:
            response = requests.get(api_url, params=params)
            if not response.ok:
                raise ConnectionError
            response_content = response.json()
        except (ConnectionError, TimeoutError):
            return None
        for record in response_content["records"]:
            username = record["username"]
            timestamp = record["timestamp"]
            timezone = record["timezone"]
            yield {
                'username': username,
                'timestamp': timestamp,
                'timezone': timezone,
            }


def get_pages_count(api_url):
    try:
        response = requests.get(api_url)
        if not response.ok:
            raise ConnectionError
        response_content = response.json()
    except (ConnectionError, TimeoutError):
        return None
    return response_content['number_of_pages']


def get_user_local_dt(user_timezone, user_timestamp):
    utc = pytz.utc
    utc_dt = utc.localize(datetime.utcfromtimestamp(user_timestamp))
    user_format_tz = timezone(user_timezone)
    user_local_dt = utc_dt.astimezone(user_format_tz)
    return user_local_dt


def is_midnighter(user_dt):
    send_check_time_from = datetime.strptime("00:00:00", "%H:%M:%S")
    send_check_time_to = datetime.strptime("04:00:00", "%H:%M:%S")
    if (send_check_time_from.time()
            <= user_dt.time()
            <= send_check_time_to.time()):
        return True


def get_midnighter_dt(user_timezone, user_timestamp):
    user_dt = get_user_local_dt(user_timezone, user_timestamp)
    if is_midnighter(user_dt):
        return user_dt


def print_title(title_was_printed):
    if not title_was_printed:
        print("Midnighters on devman detected:\n")


def print_midnighter_activity(username, user_dt):
    print("User {} sent the task for review at {}".format(
        username,
        user_dt
    ))


if __name__ == '__main__':
    api_url = "https://devman.org/api/challenges/solution_attempts/"
    pages_count = get_pages_count(api_url)
    if not pages_count:
        exit("Site {} is unavailable!".format(api_url))
    title_was_printed = False
    for attempt in load_attempts(pages_count, api_url):
        if not attempt:
            exit("Site {} is unavailable!".format(api_url))
        user_timestamp = attempt["timestamp"]
        user_timezone = attempt["timezone"]
        username = attempt["username"]
        midnighter_dt = get_midnighter_dt(user_timezone, user_timestamp)
        if midnighter_dt:
            print_title(title_was_printed)
            title_was_printed = True
            print_midnighter_activity(username, midnighter_dt)
