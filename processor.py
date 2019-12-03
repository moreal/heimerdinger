# Write some code to process matches
# FIXME: refactoring.

import db
import cassiopeia as cass

from datapipelines import NotFoundError
from collections import defaultdict

cass.apply_settings('processor-settings.json')

counts = defaultdict(int)

match_ids = db.get_timeline_ids_from_diskstore('store')

for index, match_id in enumerate(match_ids):
    try:
        match = cass.Match(id=match_id)
        match.timeline.load()
        match.load()
        game_mode = match.mode
        if game_mode in (cass.GameMode.classic, cass.GameMode.aram):
            for team in match.teams:
                for participant in team.participants:
                    # print(participant.champion.id)
                    counts[participant.champion.id] += 1
        if index != 0 and index % 2000 == 0:
            print(index, '/', len(match))

    except NotFoundError as e:
        pass
    finally:
        match_id += 1

for champion_id, count in counts.items():
    print(
        cass.Champion(id=champion_id).name,
        count)
