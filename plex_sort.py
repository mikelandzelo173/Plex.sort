#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple script that lets you log into your Plex account and select a playlist to sort.

URL: https://github.com/mikelandzelo173/Plex.sort
Python Version: 3.7+

Disclaimer:
I'm not responsible for any data loss which might occur. There may also be bugs or unexpected behaviors.
Always use with common sense.

What does it do:
You will be prompted to log into your Plex account. After that you can select a playlist that you want to sort.
Plex lacks this feature, so I made this script. It comes in handy if you want to find duplicates in a gigantic music
playlist or just want to have everything sorted alphabetically.

Before use:
You will be guided through the whole process but to skip the initial login process every time you use the script you
might want to take a note of your authentication token and save it to the config.ini file which should be located in
~/.config/plexapi/ (which can be overridden by setting the environment variable PLEXAPI_CONFIG_PATH with the file path
you desire) or in the same directory as this script. You could also save your username and password to the config.ini
file instead.

In step 2 you will have to select a resource which is connected to your Plex account. You can only select Plex Media
Servers that host playlists. If there is only one Plex Media Server available, this step will be skipped.

After that, you must select a playlist to sort. Please note that smart playlists must not be altered and therefore are
not listed. You can also determine if you want to edit the selected playlist or create a new and sorted one based on
the playlist you just selected. You can also decide by which key and direction it should be sorted and if you want to
create a new duplicated playlist instead of modifying the selected one.

For more information on the Python PlexAPI visit:
https://python-plexapi.readthedocs.io/en/latest/index.html

This project was inspired by Plex Playlist Sorter by uswemar:
https://github.com/uswemar/PlexPlaylistSorter
"""

import os
import sys

from getpass import getpass

from plexapi import PlexConfig
from plexapi.exceptions import Unauthorized
from plexapi.myplex import MyPlexAccount, MyPlexResource
from plexapi.playlist import Playlist
from plexapi.server import PlexServer
from plexapi.utils import choose


__author__ = "Michael Pölzl"
__copyright__ = "Copyright 2022, Michael Pölzl"
__credits__ = ""
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Michael Pölzl"
__email__ = "git@michaelpoelzl.at"
__status__ = "Production"


def choose_continue() -> bool:
    """
    Function: choose_continue()

    Decide on sorting another playlist.

    :returns: A boolean
    :rtype: bool
    """

    print()

    while True:
        continue_sorting = input("Do you want to sort another playlist? [Yn]")

        if not continue_sorting or continue_sorting.lower() == "y":
            return True
        elif continue_sorting.lower() == "n":
            return False


def choose_duplication() -> bool:
    """
    Function: choose_duplication()

    Decide on duplicating the selected playlist.

    :returns: A boolean
    :rtype: bool
    """

    print()

    while True:
        duplicate = input("Do you want to create a duplicated playlist instead of modifying the selected one? [yN]")

        if duplicate.lower() == "y":
            return True
        elif not duplicate or duplicate.lower() == "n":
            return False


def choose_sorting_method() -> tuple:
    """
    Function: choose_sorting_method()

    Decide on how to sort the selected playlist.

    :returns: A tuple with the key and direction to sort
    :rtype: tuple
    """

    choices = [
        {
            "name": "Sort by title, ascending",
            "key": "title",
            "reverse": False,
        },
        {
            "name": "Sort by title, descending",
            "key": "title",
            "reverse": True,
        },
        {
            "name": "Sort by sorting title, ascending",
            "key": "titleSort",
            "reverse": False,
        },
        {
            "name": "Sort by sorting title, descending",
            "key": "titleSort",
            "reverse": True,
        },
    ]

    print()
    for index, choice in enumerate(choices):
        print(f"  {index}: {choice['name']}")
    print()

    while True:
        try:
            method = input("Select sorting method: ")
            selected_choice = choices[int(method)]
            return selected_choice["key"], selected_choice["reverse"]
        except (ValueError, IndexError):
            pass


def get_account(config: PlexConfig) -> MyPlexAccount:
    """
    Function: get_account()

    Handles the Plex login process and returns a MyPlexAccount object.
    Login is handled via input prompt of username and password or by reading the config.ini file and extracting
    username and password or authentication token from there.

    :param config: PlexConfig object
    :type config: PlexConfig
    :returns: A MyPlexAccount object
    :rtype: MyPlexAccount
    """

    if config.get("auth.server_token"):
        try:
            return MyPlexAccount(token=config.get("auth.server_token"))
        except Exception:
            print("ERROR: Invalid token.")

    if config.get("auth.myplex_username") and config.get("auth.myplex_password"):
        try:
            account = MyPlexAccount(config.get("auth.myplex_username"), config.get("auth.myplex_password"))
            print(f"Your authentication token: {account.authenticationToken}")
            return account
        except Unauthorized:
            print("ERROR: Invalid email, username, or password. Please try again.")
        except Exception:
            print("ERROR: Please try again.")

    while True:
        print("Please provide your login credentials for your Plex account")
        username = input("Username: ")
        password = getpass("Password (will not be echoed): ")

        try:
            account = MyPlexAccount(username, password)
            print(f"Your authentication token: {account.authenticationToken}")
            return account
        except Unauthorized:
            print("ERROR: Invalid email, username, or password. Please try again.")
        except Exception:
            print("ERROR: Please try again.")


def get_config() -> PlexConfig:
    """
    Function: get_config()

    Checks for a config file in either the same directory as this script or in the default configuration path set via
    PLEXAPI_CONFIG_PATH in your environment.

    :returns: A PlexConfig object
    :rtype: PlexConfig
    """

    script_path = os.path.abspath(os.path.dirname(__file__))
    local_config_file = os.path.join(script_path, "config.ini")
    if os.path.exists(local_config_file):
        return PlexConfig(os.path.expanduser(local_config_file))
    else:
        return PlexConfig(os.environ.get("PLEXAPI_CONFIG_PATH", os.path.expanduser("config.ini")))


def get_playlists(server: PlexServer) -> list[Playlist]:
    """
    Function: get_playlists()

    Returns all playlists from a connected resource, filtered by smart status.

    :param server: PlexServer object
    :type server: PlexServer
    :returns: A list of Playlist objects
    :rtype: list[Playlist]
    """

    return [playlist for playlist in server.playlists() if not playlist.smart]


def get_resources(account: MyPlexAccount) -> list[MyPlexResource]:
    """
    Function: get_resources()

    Returns all resources connected to a MyPlexAccount, filtered by type. Only "Plex Media Server" items are returned.

    :param account: MyPlexAccount object
    :type account: MyPlexAccount
    :returns: A list of MyPlexResource objects
    :rtype: list[MyPlexResource]
    """

    return [resource for resource in account.resources() if resource.product == "Plex Media Server"]


def sort_playlist(
        server: PlexServer,
        playlist: Playlist,
        sort_key: str = "title",
        sort_reverse: bool = False,
        duplicate: bool = False
) -> Playlist:
    """
    Function: sort_playlist()

    Returns all resources connected to a MyPlexAccount, filtered by type. Only "Plex Media Server" items are returned.

    :param server: PlexServer object
    :type server: PlexServer
    :param playlist: Playlist object
    :type playlist: Playlistobject
    :param sort_key: The object key you want to sort the playlist by. Choices are title and titleSort.
    :type sort_key: str
    :param sort_reverse: Whether you want to sort the playlist in reverse order
    :type sort_reverse: bool
    :param duplicate: Whether you want to create a duplicated playlist instead of modifying the selected one
    :type duplicate: bool
    :returns: A Playlist object, either the modified or a newly created one
    :rtype: Playlist
    """

    # Get all items and sort them
    items = playlist.items()
    items.sort(key=lambda x: getattr(x, sort_key), reverse=sort_reverse)

    print()

    # Create a new playlist with sorted items
    if duplicate:
        new_playlist = Playlist.create(
            server=server,
            title=f"Copy of {playlist.title}",
            summary=playlist.summary,
            items=items,
            playlistType=playlist.playlistType,
        )

        print(f"Successfully created and sorted playlist {new_playlist.title}.")
        return new_playlist

    # Sort an existing playlist
    else:
        previous_item = None
        for item in items:
            playlist.moveItem(item, after=previous_item)
            previous_item = item

        print(f"Successfully sorted playlist {playlist.title}.")
        return playlist


if __name__ == '__main__':
    # Load configuration
    config = get_config()

    # Login to the Plex account
    account = get_account(config)

    # Select a resource to connect to
    resources = get_resources(account)
    resource = choose("Select resource to connect to", resources, "name")

    # Connect to the selected resource and create a server object
    server = account.resource(resource.name).connect()

    while True:
        # Select a playlist to sort
        playlists = get_playlists(server)
        playlist = choose("Select a playlist to sort", playlists, "title")

        # Select the sorting method
        sort_key, sort_reverse = choose_sorting_method()

        # Decide on duplicating the selected playlist
        duplicate = choose_duplication()

        # Sort playlist
        sort_playlist(
            server=server,
            playlist=playlist,
            sort_key=sort_key,
            sort_reverse=sort_reverse,
            duplicate=duplicate,
        )

        if not choose_continue():
            sys.exit()
