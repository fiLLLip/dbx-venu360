# DBX VENU360
Reverse engineering of the TCP protocol between the DBX VENU360 app and the DBX VENU360 hardware for control with other or custom applications. Motivation behind it was to be able to control the mute of the output or recall a preset based on either Home Assistant toggle switch or other sources. 

Using Wireshark and the DBX VENU360 app for Windows I listened for the connection procedure and certain actions I would like to perform; mainly recall presets and mute/unmute outputs.

## Package structure
There is no "one common command structure" for the payloads sent over TCP, but from what I have found out, all packages must be sent with `\n` at the end of the payload to delimit the commands. All payloads received also have this. This may stem from reusing an old serial interface/command structure, but that is only speculations. The two types of commands I have seen have a JSON structure, and a simple ascii-type style.

JSON
```
{"id":"e0bc837f-0eaa-4636-a815-7e2ea46aab87_load1","method":"Load","params":["1"]}
```
ASCII
```
set "\\Preset\ZoneGains\SV\Channel_6_Mute\" "0"
```
You can send many ASCII commands in the same payload as long as you delimit them by `\n`.

## Connection procedure
The connection procedure is pretty straight forward:
1) Client connects with TCP to <dbx_venu360_ip>:19272
2) Client sends an empty payload to the VENU360
3) VENU360 responds with `HiQnet Console` - which I guess is the signal that it is ready
4) Client logs in with `connect administrator "<password>"` - Default password is `administrator`
5) VENU360 responds `connect logged in as administrator`

Now you are ready to send commands!

## Preset recall
You can recall any preset based on the ID/number shown on the VENU360. If the display says `user preset 1` the ID of this is simply `1`.

With the connection already established, send a TCP package with the payload `{"id":"e0bc837f-0eaa-4636-a815-7e2ea46aab87_load1","method":"Load","params":["1"]}` and the VENU360 starts responding with several packages containing the same `id` as in you command. This seems to be to track the request to the responses. The first argument in `params` is the ID/number of the preset to recall. Typical responses to this is:
```
{"done":false,"error":null,"id":"e0bc837f-0eaa-4636-a815-7e2ea46aab87_load1","result":"Load [1]: loaded from db"}

{"done":false,"error":null,"id":"e0bc837f-0eaa-4636-a815-7e2ea46aab87_load1","result":"- Load [1.6]: builder is done"}

{"done":false,"error":null,"id":"e0bc837f-0eaa-4636-a815-7e2ea46aab87_load1","result":"- Reconfig Complete- Load [2]: configure"}

{"error":null,"id":"e0bc837f-0eaa-4636-a815-7e2ea46aab87_load1","result":"- Load [3]: loaded sv settings"}
```
You can also subscribe to the progressbar that is shown on the display with the command `sub "\\Node\Config\SV\Progress\"`. This will then reply during the recall with payloads like `set "\\Node\Config\SV\Progress" "0.716037"`
## Mute/Unmute outputs
To mute an output, simply send a set command with the output channel number, and 0 or 1 for unmute and mute. Structure is like:

`set "\\Preset\ZoneGains\SV\Channel_<channel>_Mute\" "<0/1>"`

For instance to mute channel 6:

`set "\\Preset\ZoneGains\SV\Channel_6_Mute\" "1"`

and the VENU360 will respond with a result:

`setr "\\Preset\ZoneGains\SV\Channel_6_Mute" "On"`

# Home Assistant and Node-RED
![Node-RED flow](/node-red.png)
I have experimentet with using the findings in Home Assistant and Node-RED. Here I have added a helper called `input_boolean.delay` to simulate turning on/off the outputs to the delayed zone on the VENU360.

This flow connects on deployment to he hard coded IP set in the TCP node, and can then react to the changes of the input_boolean which I can toggle in the either LoveLace or from automations.

[The flow is of course also added to this repo](/node-red-flow.json)

# Python sample
In the [python-sample](/python-sample) folder, there are some samples on how you can interact using Python. I have created 3 different samples:
- get_preset_names.py - fetches the names of all the stored presets along with its ID/number
- recall_preset.py - recalls the preset based on an ID/number
- mute_output.py - mute/unmute an output

## Usage
```
python3 get_preset_names.py <ip>

# <mute>: 0 for unmute, 1 for mute
python3 mute_output.py <ip> <channel> <mute>

python3 recall_preset.py <ip> <preset>
```