from googleapiclient.discovery import build
from secrets import calendar_id, api_key
from datetime import datetime as dt, timedelta
import json # just for debugging
import sys


def get_events():
    now = dt.now().isoformat().split('.')[0] + '+03:00'

    with build('calendar', 'v3', developerKey=api_key) as service:
        response = service.events().list(calendarId=calendar_id, timeMin=now).execute() # get events
        events = response['items']
        instances = []

        for original in events:
            response = service.events().instances(calendarId=calendar_id, eventId=original['id'], timeMin=now).execute() # get events
            if response['items']:
                instances += response['items']
            else:
                if original['status'] == 'cancelled':
                    continue
                instances.append(original)

        return instances


def get_upcoming():
    event_list = set()

    for event in get_events():
        if 'start' in event:
            start = event['start']['dateTime'].split(':')[:2]
            end = event['end']['dateTime'].split(':')[:2]
            title = event['summary'] if 'summary' in event else 'untitled'

            start = ':'.join(start)
            end = ':'.join(end)
            title = title.lower()

            event_list.add(f'{title} from {start} to {end}')

    return list(event_list)


def parse_args(default):
    args = sys.argv
    if len(args) <= 1:
        return default[2:]
    fmt = '--'.join(args[1:])
    return fmt[2:] # cut off the --


def earliest(events):
    now = dt.now().isoformat().split('.')[0]

    events = [(e.split(' from ')[1].split(' to ')[0], e) for e in events]
    events = [e for e in events if e[0] > now]
    events = sorted(events, key=lambda x: x[0])

    return events[0][1] 


def main(fmt = 'full'):
    events = get_upcoming()
    if 'single' in fmt:
        events = [earliest(events)]
    for event in events:
        if 'full' in fmt:
            print(event.replace('T', ' at '))
        elif 'dtonly' in fmt:
            print(event.split(' from ')[1].replace('to', '-'))
        elif 'startonly' in fmt:
            print(event.split(' from ')[1].split(' to ')[0])
        elif 'endonly' in fmt:
            print(event.split(' from ')[1].split(' to ')[1])
        else:
            print('Supported formats: full, dtonly, startonly, endonly')
            exit(1)


if __name__ == '__main__':
    main(parse_args(default='--full'))
