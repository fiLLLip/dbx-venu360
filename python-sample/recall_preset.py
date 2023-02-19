import sys
import uuid

from venu360 import send_and_receive, connect

HOST = sys.argv[1]
PRESET = sys.argv[2]

if not PRESET.isnumeric():
    print(f'Argument is not a number, got: {PRESET}')
    exit()

# Connect to the venu360
with connect(HOST) as sock:
    send_and_receive(sock, f'{{"id":"{uuid.uuid4()}_load{PRESET}","method":"Load","params":["{PRESET}"]}}') # Recall given preset
    send_and_receive(sock, f'{{"id":"{uuid.uuid4()}_load{PRESET}","method":"Load","params":["{PRESET}"]}}') # Recall given preset
