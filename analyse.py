import json

def is_good(room):
    return room['score'] >= 4.5 \
        and room['reviews'] >= 20


with open('booking_rooms.json') as f:
    rooms = json.load(f)


rooms = [room for room in rooms if is_good(room)]
print(f'Found {len(rooms)} rooms')
