"""
This library contains all the functions related to albums.
"""
from pprint import pprint
import random
from typing import List

from app import helpers, instances, models
from app.lib import taglib
from tqdm import tqdm


def get_all_albums() -> List[models.Album]:
    """
    Returns a list of album objects for all albums in the database.
    """
    print("Getting all albums...")

    albums: List[models.Album] = []

    db_albums = instances.album_instance.get_all_albums()

    for album in tqdm(db_albums, desc="Creating albums"):
        aa = models.Album(album)
        albums.append(aa)

    return albums


def validate() -> None:
    """
    Creates album objects for all albums and returns
    a list of track objects
    """


def find_album(albums: List[models.Album], hash: str) -> int | None:
    """
    Finds an album by album title and artist.

    :param `albums`: List of album objects.
    :param `hash`: Hash of album.
    :return: Index of album in list.
    """

    left = 0
    right = len(albums) - 1

    while left <= right:
        mid = (left + right) // 2

        if albums[mid].hash == hash:
            return mid

        if albums[mid].hash < hash:
            left = mid + 1
        else:
            right = mid - 1

    return None


def get_album_duration(album: List[models.Track]) -> int:
    """
    Gets the duration of an album.
    """

    album_duration = 0

    for track in album:
        album_duration += track.length

    return album_duration


def use_defaults() -> str:
    """
    Returns a path to a random image in the defaults directory.
    """
    path = "defaults/" + str(random.randint(0, 20)) + ".webp"
    return path


def gen_random_path() -> str:
    """
    Generates a random image file path for an album image.
    """
    choices = "abcdefghijklmnopqrstuvwxyz0123456789"
    path = "".join(random.choice(choices) for i in range(20))
    path += ".webp"

    return path


def get_album_image(album: list) -> str:
    """
    Gets the image of an album.
    """

    for track in album:
        img_p = gen_random_path()

        exists = taglib.extract_thumb(track["filepath"], webp_path=img_p)

        if exists:
            return img_p

    return use_defaults()


class GetAlbumTracks:
    """
    Finds all the tracks that match a specific album, given the album title
    and album artist.
    """

    def __init__(self, tracklist: List[models.Track], albumhash: str) -> None:
        self.hash = albumhash
        self.tracks = tracklist
        self.tracks.sort(key=lambda x: x.albumhash)

    def __call__(self):
        tracks = helpers.UseBisection(self.tracks, "albumhash", [self.hash])()

        pprint(tracks)

        # while index is not None:
        #     track = self.tracks[index]
        #     tracks.append(track)
        #     self.tracks.remove(track)
        #     index = helpers.UseBisection(self.tracks, "albumhash", [self.hash])()

        return tracks


def get_album_tracks(tracklist: List[models.Track], hash: str) -> List:
    return GetAlbumTracks(tracklist, hash)()


def create_album(track: dict, tracklist: list[models.Track]) -> dict:
    """
    Generates and returns an album object from a track object.
    """
    album = {
        "title": track["album"],
        "artist": track["albumartist"],
    }
    albumhash = helpers.create_album_hash(album["title"], album["artist"])
    album_tracks = get_album_tracks(tracklist, albumhash)

    if len(album_tracks) == 0:
        return None

    album["date"] = album_tracks[0]["date"]

    album["image"] = get_album_image(album_tracks)
    # album["image"] = "".join(x for x in albumhash if x not in "\/:*?<>|")

    return album
