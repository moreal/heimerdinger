from functools import reduce
from enum import Enum

import db

class ItemEvent(Enum):
    Purchased = 'Purchased'
    Sold = "Sold"
    Undo = "Undo"


def parse_purchase_history(match_data: dict, timeline_data: dict) -> dict:
    if match_data['gameMode'] != 'CLASSIC':
        return
    players = {participant['participantId']: participant['player'] for participant in match_data['participantIdentities']}
    participants = match_data['participants']
    events = (event for frame in timeline_data['frames'] for event in frame['events'])

    get_champion = lambda x: participants[x-1]['championId']
    get_champion_name = lambda x: db.load_champion_table()[x]['name']
    get_lane = lambda x: participants[x-1]['timeline']['lane']

    activities = dict()
    for event in events:
        event_type = event['type']
        if event_type.startswith('ITEM'):
            player_id = event['participantId']
            champion_id = get_champion(player_id)
            champion_name = get_champion_name(champion_id)
            lane = get_lane(player_id)
            key = (player_id, champion_name, lane)

            timestamp = event['timestamp']
            detail_type = event_type[5:]
            activity = activities.get(key, list())

            if detail_type == 'UNDO':
                activity.pop()
            elif detail_type == "PURCHASED":
                activity.append((ItemEvent.Purchased, event['itemId'], timestamp))
            elif detail_type == "SOLD":
                activity.append((ItemEvent.Sold, event['itemId'], timestamp))

            activities[key] = activity
    return activities

if "__main__" == __name__:
    match_data = db.load_match_data(4000696305)
    timeline_data = db.load_timeline_data(4000696305)
    for key, histories in parse_purchase_history(match_data, timeline_data).items():
        print(key)
        for history in histories:
            item_event, item_id = history
            print(item_event.value, db.load_item_table()[item_id]['name'])
