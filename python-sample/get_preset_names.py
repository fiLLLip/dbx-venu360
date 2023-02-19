from collections import OrderedDict
import sys
import uuid
import json

from venu360 import send_and_receive, connect

HOST, PORT = sys.argv[1], 19272

# Connect to the venu360
with connect(HOST) as sock:
    data = send_and_receive(sock, f'{{"id":"{uuid.uuid4()}_getPresetNames","method":"Get","params":["1", "100", "presetName"]}}') # Get preset names
    jason = json.loads(data)
    numerized = OrderedDict(sorted(jason['result'].items(), key=lambda t: int(t[0])))
    for id, name in numerized.items():
        print(f'{id}: {name}')

