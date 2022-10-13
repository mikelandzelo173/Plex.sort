Plex.sort
=========

Plex.sort is a simple script that lets you log into your Plex account and select a playlist to sort.

Currently, Python 3.7+ is supported.

## Quickstart

1. Make sure [pip](https://pip.pypa.io/en/stable/installation/) is installed on your machine.

2. Create a virtual environment and activate it (optional), e.g.:
```bash
pip install virtualenv
python3 -m venv venv
source venv/bin/activate
```

3. Install the packages from the `requirements.txt` file using pip:
```bash
pip install -r requirements.txt
```

4. Execute the script and follow the guidance
```bash
./plex_sort.py
```

## Example usage

```bash
(venv) ➜ Plex.sort ./plex_sort.py

  0: PlexServerHome
  1: NAS1337
  2: Another Storage Resource

Select resource to connect to: 1

  0: Favorite music
  1: Movies to watch
  2: Random hits
  3: X-mas songs

Select a playlist to sort: 3

  0: Sort by title, ascending
  1: Sort by title, descending
  2: Sort by sorting title, ascending
  3: Sort by sorting title, descending

Select sorting method: 0

Do you want to create a duplicated playlist instead of modifying the selected one? [yN]

Successfully sorted playlist X-mas songs.
```

## Configuration options

To skip the initial login process every time you use the script you might want to take a note of your authentication
token after your first login and save it to the config.ini file which should be located in `~/.config/plexapi/`
(which can be overridden by setting the environment variable `PLEXAPI_CONFIG_PATH` with the file path you desire) or in
the same directory as this script. Instead of the token you could also save your username and password to the
`config.ini` file.

Instead of the token you could also save your username and password to the `config.ini` file.

```ini
[auth]
myplex_username = JohnDoe
myplex_password = MyR4nd0mPassword
server_token = AjsUeO6Bk89BQPdu5Dnj
```
