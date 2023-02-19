import sys

from venu360 import send_and_receive, connect

HOST, PORT = sys.argv[1], 19272
CHANNEL = sys.argv[2]
MUTE = sys.argv[3]

if not CHANNEL.isnumeric():
    print(f'Argument is not a number, got: {CHANNEL}')
    exit()

# Connect to the venu360
with connect(HOST) as sock:
    send_and_receive(sock, f'set "\\\Preset\\ZoneGains\\SV\\Channel_{CHANNEL}_Mute\\" "{MUTE}"') # Mute or unmute channel output
