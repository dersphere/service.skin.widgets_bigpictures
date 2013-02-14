#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2013 Tristan Fischer (sphere@dersphere.de)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import random

import xbmc
import xbmcgui

from thebigpictures import ScraperManager

DEBUG = True
MAX_ITEMS = 20
PROPERTY_PREFIX = 'bigpictures'

WINDOW = xbmcgui.Window(10000)


def set_random_album():
    clear_properties()
    scraper_manager = ScraperManager()

    scraper_manager.shuffle()
    scraper_manager.next()
    albums = scraper_manager.get_albums()
    album = random.choice(albums)
    photos = scraper_manager.get_photos(album['album_url'])

    set_property('scraper.title', scraper_manager.current_scraper.title)
    set_property('scraper.id', str(scraper_manager.current_scraper._id))
    set_property('album.title', album['title'])
    set_property('album.url', album['album_url'])
    set_property('album.photo_count', str(min(len(photos), MAX_ITEMS)))
    for i, photo in enumerate(photos):
        for key in ('pic', 'description', 'title'):
            set_property('photo.%d.%s' % (i, key), photo[key])
        if i + 1 == MAX_ITEMS:
            break
    if DEBUG:
        xbmc.executebuiltin('XBMC.Notification("Done", "TBP Widget", 1000)')


def clear_properties():
    current_len = get_property('album.photo_count')
    if current_len:
        current_len = int(current_len)
        for i in xrange(current_len):
            for key in ('pic', 'description', 'title'):
                clear_property('photo.%d.%s' % (i, key))
            if i + 1 == MAX_ITEMS:
                break


def set_property(key, value):
    key = '%s.%s' % (PROPERTY_PREFIX, key)
    if DEBUG:
        log(u'[%s] -> %s' % (key, repr(value)))
    WINDOW.setProperty(key, value.encode('utf-8'))


def get_property(key):
    key = '%s.%s' % (PROPERTY_PREFIX, key)
    return WINDOW.getProperty(key)


def clear_property(key):
    key = '%s.%s' % (PROPERTY_PREFIX, key)
    if DEBUG:
        log(u'[%s] -> cleared' % key)
    return WINDOW.clearProperty(key)


def log(text):
    xbmc.log(u'TheBigPictures Widget: %s' % text)


if __name__ == '__main__':
    log('started')
    set_random_album()
    log('exited')
