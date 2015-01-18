#!/usr/bin/env python

"""getalb
Script for downloading entire albums at once from http://musicmp3spb.org,
as opposite to song-by-song manual downloading.
Downloaded files are stored in 'getalb/music/' directory.
Script works with Python 2.7.
Script uses BeautifulSoup library for parsing html pages.
"""

__author__ = 'Oleg Esenkov (oleges@list.ru)'
__copyright__ = 'Copyright (c) 2015 Oleg Esenkov'
__license__ = 'The MIT License (MIT)'
__version__ = '0.2.3'

import argparse
import os
import re
import sys
import time
import urllib
import urllib2

from bs4 import BeautifulSoup

TARGET_SITE = 'http://musicmp3spb.org'


def get_url():
    """Return album url string from command line argument or,
    if argument not given, from user input."""
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('album_url', nargs='?', default=None,
                                 help='full album url from ' + TARGET_SITE)
    arguments_given = argument_parser.parse_args()
    if arguments_given.album_url:
        album_url = arguments_given.album_url
    else:
        album_url = raw_input('Full album url from ' + TARGET_SITE + ':\n')
    return album_url


def web_request(url, form_data=None):
    """Return response object to GET or POST request."""
    if form_data:  # Should be encoded only if not None
        form_data = urllib.urlencode(form_data)
    request = urllib2.Request(url, form_data)
    connect_count = 0
    connect_attempts = 5
    while connect_count < connect_attempts:
        try:
            response = urllib2.urlopen(request)
            return response
        except urllib2.URLError:
            print 'Connection failed. Trying again...'
            connect_count += 1
            time.sleep(1)
        except ValueError:
            raw_input('Wrong url. Could not connect. Press ENTER to exit.')
            sys.exit()
    raw_input('Check your internet connection. Press ENTER to exit.')
    sys.exit()


def parse_page(response):
    """Return parsed page object."""
    html_page = response.read()
    parsed_page = BeautifulSoup(html_page)
    return parsed_page


def get_album_name(parsed_album_page):
    """Return album name string."""
    try:
        album_name_div = parsed_album_page.find('div', 'Name')
        album_name = album_name_div.contents[0].replace('\n', '')
        return album_name
    except AttributeError:
        raw_input('Wrong url. No album found. Press ENTER to exit.')
        sys.exit()


def get_temporary_links(parsed_album_page):
    """Return list of temporary links to songs."""
    temporary_links = []
    try:
        songs_div = parsed_album_page.find('div', 'albSong')
        songs_relative_links_list = songs_div.find_all('a', 'Name')
        for link in songs_relative_links_list:
            temporary_links.append(TARGET_SITE + link.get('href'))
        return temporary_links
    except AttributeError:
        raw_input('Wrong url. No songs found. Press ENTER to exit.')
        sys.exit()


def get_form_data(parsed_temp_page):
    """Return form data as a dictionary."""
    data_name = 'robot_code'
    form_data_element = parsed_temp_page.find('input', {'name': data_name})
    data_value = form_data_element.get('value')
    form_data = {data_name: data_value}
    return form_data


def get_song_link(parsed_song_page):
    """Return song url string."""
    song_link_element = parsed_song_page.find(href=re.compile('tempfile.ru'))
    song_link = song_link_element.get('href')
    return song_link


def download_song(song_link):
    """Download file with progress percentage."""
    downloaded_size = 0
    block_size = 8192
    backspace_code = '\x08'
    song_file = web_request(song_link)
    metadata = song_file.info()
    file_size = int(metadata.getheaders('Content-Length')[0])
    file_name = metadata.getheaders('Content-Disposition')[0].split('\"')[1]
    file_not_exists = not os.path.isfile(file_name)
    if file_not_exists or (os.stat(file_name).st_size != file_size):
        downloading_not_finished = True
        output_file = open(file_name, 'wb')
        print 'File: {0}\nSize: {1} bytes\nDownloading...'.format(file_name,
                                                                  file_size),
        while downloading_not_finished:
            next_file_block = song_file.read(block_size)
            if next_file_block:  # Not empty
                output_file.write(next_file_block)
                downloaded_size += len(next_file_block)
                percentage = '{0}%'.format(downloaded_size * 100 / file_size)
                print percentage + backspace_code * (len(percentage) + 1),
            else:
                print  # Newline
                downloading_not_finished = False
        output_file.close()


def main():
    album_url = get_url()
    print 'Connecting...'
    album_page = web_request(album_url)
    parsed_album_page = parse_page(album_page)
    album_name = get_album_name(parsed_album_page)
    print 'Album: ' + album_name
    temporary_links = get_temporary_links(parsed_album_page)
    print 'Found {0} file(s)'.format(len(temporary_links))
    
    music_dir = os.path.dirname(os.path.realpath(__file__)) + '/music'
    music_dir_not_exists = not os.path.exists(music_dir)
    if music_dir_not_exists:
        os.mkdir(music_dir)
    
    os.chdir(music_dir)
    album_dir_not_exists = not os.path.exists(album_name)
    if album_dir_not_exists:
        os.mkdir(album_name)
    os.chdir(album_name)
    for link in temporary_links:
        temp_page = web_request(link)
        parsed_temp_page = parse_page(temp_page)
        redirected_url = temp_page.geturl()
        form_data = get_form_data(parsed_temp_page)
        song_page = web_request(redirected_url, form_data)
        parsed_song_page = parse_page(song_page)
        song_link = get_song_link(parsed_song_page)
        download_song(song_link)
    raw_input('All files downloaded successfully. Press ENTER to exit.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raw_input('\nAborting... Press ENTER to exit.')
        sys.exit()
