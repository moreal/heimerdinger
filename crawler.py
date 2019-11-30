import os
import json
import time
import requests

from process import parse_purchase_history

start_time = time.time()

max_limit = 100
limit_count = 1
API_KEY = "KEY"

def increase_count():
    global limit_count, start_time, max_limit
    limit_count += 1
    if limit_count == max_limit:
        used_time = 120 - (time.time() - start_time)
        print('[!] wait for ', used_time)
        time.sleep(120 - (time.time() - start_time))
        start_time = time.time()
        limit_count = 1


def get_match_timelines(match_id: int) -> dict:
    ENDPOINT = f"https://kr.api.riotgames.com/lol/match/v4/timelines/by-match/{match_id}"
    resp = requests.get(ENDPOINT, headers={
        "X-Riot-Token": API_KEY,
    })
    increase_count()
    return resp.status_code, resp.json()


def get_match_info(match_id: int) -> dict:
    ENDPOINT = f"https://kr.api.riotgames.com/lol/match/v4/matches/{match_id}"
    resp = requests.get(ENDPOINT, headers={
        "X-Riot-Token": API_KEY,
    })
    increase_count()
    return resp.status_code, resp.json()


def get_matches_from_local(path: str) -> set:
    return set(map(lambda x: int(x[:-5]), os.listdir(path)))


def check_status_code(status_code: int) -> bool:
    if status_code == 200:
        return True
    else:
        print(f'[-] Failed, because status_code was {status_code}')
        return False

match_id = max(get_matches_from_local('./timelines')) + 1

# FIXME: refactoring.
while True:
    print(f'[+] Try {match_id}..., {limit_count}/{max_limit}')
    status_code, match_data = get_match_info(match_id)
    
    if check_status_code(status_code):
        print(f'[+] Save {match_id}...')
        with open(f'matches/{match_id}.json', 'w') as f:
            json.dump(match_data, f, indent=2)

        status_code, timeline_data = get_match_timelines(match_id)
        if check_status_code(status_code):
            with open(f'timelines/{match_id}.json', 'w') as f:
                json.dump(timeline_data, f, indent=2)
            histories = parse_purchase_history(match_data, timeline_data)
            print(histories)
    match_id += 1
