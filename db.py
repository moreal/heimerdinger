import os
import json
import requests

items = None
champions = None

def load_match_data(match_id: int) -> dict:
    with open(f'matches/{match_id}.json', 'r') as f:
        return json.load(f)


def load_timeline_data(match_id: int) -> dict:
    with open(f'timelines/{match_id}.json', 'r') as f:
        return json.load(f)


def load_item_table(*, version: str='9.23.1', language: str='ko_KR') -> dict:
    global items
    if items is None:
        ENTRYPOINT = f'http://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/item.json'
        items = requests.get(ENTRYPOINT).json()['data']
        items = {int(key): value for key, value in items.items()}
    return items


def load_champion_table(*, version: str='9.23.1', language: str='ko_KR') -> dict:
    global champions
    if champions is None:
        ENTRYPOINT = f'http://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/champion.json'
        champions = requests.get(ENTRYPOINT).json()['data']
        champions = {int(champion['key']): champion for champion in champions.values()}
    return champions


def get_timeline_ids_from_diskstore(path: str) -> list:
    return list(map(lambda x: int(x[15:]), filter(lambda x: x.startswith('TimelineDto.KR'), os.listdir('./store'))))
