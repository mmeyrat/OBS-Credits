# OBS Credits

A small script made with Python 3.6 for OBS 21.0+. It fetches a list of followers from a specified Twitch account. Only the last 100 followers are retrieved. Then, the list is formatted in a Text Source to form a credit sequence.
The script is activated when the specified Scene becomes active.

A `config.py` file is necessary and must contain a Twitch API authentification token, and a client ID for a Twitch API application.

There are 3 parameters :
- `Streamer ID`, the numeral ID corresponding to the streamer's account.
- `Text Source`, the destination Text Source in which the credits will be put.
- `Scene`, the scene that triggers the update of the Text Source.
