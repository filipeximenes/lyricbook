#!/usr/bin/env python

import sys
from datetime import datetime
import json
import hashlib
from bs4 import BeautifulSoup
import requests


BACKUPS_PATH = "backups"
METADATA_FILE_NAME = "lyrics.json"
SOURCES_FILE_NAME = "sources.json"
NOW = datetime.now().isoformat()


def hash_source_url(url):
    return hashlib.md5(url.encode()).hexdigest()


def parse_song(url):
    resp = requests.get(url)

    soup = BeautifulSoup(resp.content, features="html.parser")

    article = soup.article

    song_name = article.h1.text.strip()
    artist = article.h2.text.strip()

    lyric_html = article.find_all("div", {"class": "cnt-letra-trad"})[0]
    strophes_html = lyric_html.find_all('p')

    lyric = []
    for strophe in strophes_html:
        verses = strophe.get_text(separator='|||').split('|||')
        lyric.append(verses)

    return {
        "title": song_name,
        "artist": artist,
        "url": url,
        "lyrics": lyric,
        "last_updated": NOW,
    }


def read_json_file(file_name):
    try:
        with open(file_name) as metadata_file:
            metadata = json.loads(metadata_file.read())
    except FileNotFoundError:
        metadata = {}
    return metadata


def write_json_file(file_name, data):
    with open(file_name, "w+") as metadata_file:
        metadata_file.write(json.dumps(data, indent=2))


def read_metadata():
    return read_json_file(METADATA_FILE_NAME)


def write_metadate(metadata):
    return write_json_file(METADATA_FILE_NAME, metadata)


def backup():
    metadata = read_metadata()
    write_json_file(f"{BACKUPS_PATH}/{NOW}.json", metadata)


def update_song(song_url):
    backup()

    metadata = read_metadata()

    url_hash = hash_source_url(song_url)
    parsed_song = parse_song(song_url)
    metadata[url_hash] = parsed_song

    write_metadate(metadata)


def process_lyrics():
    backup()

    metadata = read_metadata()

    song_urls = read_json_file(SOURCES_FILE_NAME)

    for song_url in song_urls:
        url_hash = hash_source_url(song_url)

        if url_hash in metadata:
            print("OK", url_hash, song_url)
            continue

        print("FETCHING", url_hash, song_url)

        parsed_song = parse_song(song_url)

        metadata[url_hash] = parsed_song

    write_metadate(metadata)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_song(sys.argv[1])
    else:
        process_lyrics()
