import db
import cassiopeia as cass

from datapipelines import NotFoundError

cass.apply_settings('settings.json')

match_id = max(db.get_timeline_ids_from_diskstore('store')) + 1

while True:
    try:
        print("[+] Try to load", match_id)
        match = cass.Match(id=match_id)
        match.timeline.load()
        match.load()
        print("[!] Success to load!", match.creation.to('local'), '~', (match.creation + match.duration).to('local'))
    except NotFoundError as e:
        print("[!] Not found!")
    finally:
        match_id += 1
