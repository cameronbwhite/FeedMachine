# Copyright (C) 2013, Cameron White
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the project nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE PROJECT AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE PROJECT OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import feedparser
import pickle
import logging
import sys
import scripts

class FeedDB(object):
    """Summary of class

    Longer class information...
    Longer class information...

    Attributes:
        _database_filename:

    """

    def __init__(self, database_filename):
        """ Summary of __init__

        Args:
            database_filename: Filename of SQL database.
        """
        self._database_filename = database_filename
        self._create_tables()

    def __iter__(self):
        """ docstring for getFeed """

        feeds = self.get_all_feeds()

        for i in feeds:
            yield i

    def __len__(self):
        """ Return the number of feeds """

        try:
            with sqlite3.connect(self._database_filename) as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT COUNT(*) FROM feeds')
                return cursor.fetchone()[0]

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

    def add_feed(self, location):
        """ Add a feed

        Args:
            location: The url or file of the feed

        """

        try: 
            with sqlite3.connect(self._database_filename) as connection:

                cursor = connection.cursor()

                d = feedparser.parse(location)

                cursor.execute('''
                    INSERT INTO feeds 
                        (location, feed) 
                    VALUES 
                        (?, ?)
                    ''', 
                        (location, pickle.dumps(d))
                    ) 

                connection.commit()

        except sqlite3.IntegrityError:
            logging.info('Feed already exists: ' + location)

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

        else:
            logging.info('Added feed:' + location)

    def add_script(self, feed_id, script, options):
        """ Attach a script to a feed. 

        Long Description

        Args:
            feed_id:    The id of feed the attach the script.
            script:   The script that runs/implements the script.
            options:      The kargs to pass to the script script.

        """
        try:    
            with sqlite3.connect(self._database_filename) as connection:
                
                cursor = connection.cursor()

                l = [feed_id]
                l.append(pickle.dumps(script) if script else None)
                l.append(pickle.dumps(options) if options else None)   

                cursor.execute('''
                    INSERT INTO scripts
                        (feed_id, script, options)
                    VALUES
                        (?, ?, ?)
                    ''', l ) 

                connection.commit()

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

        else:
            logging.info('Added script ' + str(script.__name__) + ' to ' + str(feed_id))

    def get_all_feeds(self):
        """ Return a list of all the feeds.

        Returns:
            The returned list contains a tuple for every feed.
            The first item in the tuple is the feed's id, the
            second item is the location (url/filename) of the
            feed, and the last item is the parsed feed.

        """

        try: 
            with sqlite3.connect(self._database_filename) as connection:

                cursor = connection.cursor()

                cursor.execute('''
                    SELECT feed_id, location, feed FROM feeds
                    ''')
                
                rows = cursor.fetchall() 

                l = []
                for r in rows:
                    l.append({'feed_id'  : r[0],
                              'location' : r[1],
                              'feed'     : pickle.loads(r[2])
                             })

                return l

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

    def get_all_scripts(self):
        """ Get all scripts

        Returns:
            List of all the scripts
        """
        try:
            with sqlite3.connect(self._database_filename) as connection:

                cursor = connection.cursor()

                cursor.execute('''
                    SELECT script_id, feed_id, script, options
                    FROM scripts
                    ''') 

                l = []
                for i in cursor.fetchall():
                    l.append({'script_id' : i[0],
                              'feed_id'   : i[1],
                              'script'    : pickle.loads(i[2]),
                              'options'   : pickle.loads(i[3]) if i[3] else None,
                              })

                return l

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e


    def get_feed_scripts(self, feed_id):
        """ Get a list of scripts attach to the feed.

        Args:
            feed_id: The id of the feed.

        Returns:
           List of the scripts. 

        """

        try:
            with sqlite3.connect(self._database_filename) as connection:

                cursor = connection.cursor()

                cursor.execute('''
                    SELECT script_id, feed_id, script, options
                    FROM scripts
                    WHERE feed_id == ?
                    ''', str(feed_id) ) 

                l = []
                for i in cursor.fetchall():
                    l.append({'script_id' : i[0],
                              'feed_id'   : i[1],
                              'script'    : pickle.loads(i[2]),
                              'options'   : pickle.loads(i[3]) if i[3] else None,
                              })

                return l

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e


    def get_feed(self, feed_id):


        try:
            with sqlite3.connect(self._database_filename) as connection:

                cursor = connection.cursor()

                cursor.execute('''
                    SELECT feed_id, location, feed
                    FROM feeds
                    WHERE feed_id == ?
                    ''', str(feed_id) )

                t = cursor.fetchone()

                return {'feed_id'  : t[0],
                        'location' : t[1],
                        'feed'     : pickle.loads(t[2])
                        }

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

        except TypeError:
            return None

    def get_parsed_entries_guids(self, feed_id):
        """ get a list of parsed entries guids for the feed.

        Args:
            feed_id: The id of the feed.

        Returns:
            A list of parsed entries guids.

        """

        try:
            with sqlite3.connect(self._database_filename) as connection:

                cursor = connection.cursor()

                cursor.execute('''
                    SELECT guid FROM parsed_feeds WHERE feed_id == ?
                    ''', str(feed_id))

                l = []
                for i in cursor.fetchall():
                    l.append(i[0]) 

                return l

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

    # TODO: Remove     
    def print_feed_list(self):

        for feed in self:

            print('feed_id:' + str(feed['feed_id']))
            print('\t' + 'Title: ' + str(feed['feed'].feed.title))
            print('\t' + 'Location: ' + str(feed['location']))
            print('\t' + 'Description: ' + str(feed['feed'].feed.description))

    def remove_feed_by_id(self, feed_id):
        """ summary of remove_feed_by_id 

        Args:
            feed_id:    The id of the feed.

        Raises:

        """

        try:
            with sqlite3.connect(self._database_filename) as connection:

                cursor = connection.cursor()

                cursor.execute('''
                    DELETE FROM feeds
                    WHERE feed_id == ?
                    ''', str(feed_id) )

                logging.debug(debug_info() + 'Deleted feed (' + \
                              feed_id + ' from feeds')

                cursor.execute('''
                    DELETE FROM parsed_feeds
                    WHERE feed_id == ?
                    ''', str(feed_id) )

                logging.debug(debug_info() + 'Deleted feed (' + \
                              feed_id + ' from parsed_feeds')

                cursor.execute('''
                    DELETE FROM scripts
                    WHERE feed_id == ?
                    ''', str(feed_id) )

                logging.debug(debug_info() + 'Deleted feed (' + \
                              feed_id + ' from scripts')

                connection.commit()

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

    def remove_script_by_id(self, script_id):
        """ remove a script by its id.

        Args:
            script_id: The id of the script

        """

        try:
            with sqlite3.connect(self._database_filename) as connection:
                
                cursor = connection.cursor()

                cursor.execute('''
                    DELETE FROM scripts
                    WHERE script_id == ?
                    ''', str(script_id) )

                connection.commit()

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

    def set_parsed(self, feed_id, guid):
        """ Set a entry in a feed as parsed.

        Args:
            feed_id:    The id of the feed.
            guid:       The guid of a entry in the feed.

        """

        try:
            with sqlite3.connect(self._database_filename) as connection:
                
                cursor = connection.cursor()

                cursor.execute('''
                    INSERT INTO parsed_feeds 
                        (feed_id, guid)
                    VALUES (?, ?)
                    ''', (feed_id, guid) )

                connection.commit()

        except sqlite3.IntegrityError:
            logging.info('feed (' + str(feed_id) + ') guid (' + str(guid) + 
                         ') is already set as parsed.')

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e


    def run_scripts(self, feed_id):
        
        try:  
            with sqlite3.connect(self._database_filename) as connection:
                
                cursor = connection.cursor()

                scripts = self.get_feed_scripts(feed_id)

                for d in scripts:
                    script = d['script']
                    args = d['args']
                    options = d['options'] 
                    script(self, feed_id, args, options)

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

        except KeyError:
            pass

    def sqlite_version(self):
        """ Return a string of the sqlite version """

        try:
            with sqlite3.connect(_database_filename) as connection:
                
                cursor = connection.cursor()
                cursor.execute('SELECT SQLITE_VERSION()')
                return cursor.fetchone()[0]

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

    def unset_parsed(self, feed_id, guid):
        """ Unset a entry in a feed as parsed.

        Args:
            feed_id:    The id of the feed.
            guid:       The guid of a entry in the feed.

        """

        try: 
            with sqlite3.connect(self._database_filename) as connection:
                
                cursor = connection.cursor()

                cursor.execute('''
                    DELETE FROM parsed_feeds
                    WHERE feed_id == ? AND guid == ?
                    ''', (str(feed_id), str(guid)) )

                connection.commit()

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

    def update_all_feeds(self):
        """ update all feeds """

        try: 
            with sqlite3.connect(self._database_filename) as connection:
                
                cursor = connection.cursor()

                cursor.execute('''
                    SELECT feed_id, location, feed FROM feeds
                    ''')

                feeds = cursor.fetchall()
                connection.commit()

            for f in feeds:
                feed_id, location, feed = f[0], f[1], f[2]
                d = feedparser.parse(location)
                self.update_feed(feed_id, d)
                self.run_scripts(feed_id)

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

    def update_feed(self, feed_id, new_feed):

        try: 
            with sqlite3.connect(self._database_filename) as connection:
                
                cursor = connection.cursor()

                cursor.execute('''
                    UPDATE feeds
                    SET feed = ?
                    WHERE feed_id == ?
                    ''', (pickle.dumps(new_feed), str(feed_id)))

                connection.commit()

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

    def _create_tables(self):
        """ Create all the sqlite tables. """

        try:
            with sqlite3.connect(self._database_filename) as connection:
                
                cursor = connection.cursor()

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS feeds (
                        feed_id     INTEGER PRIMARY KEY, 
                        location    TEXT UNIQUE,
                        feed        BLOB)
                    ''')

                logging.debug(debug_info() + 'Created table:' + 'feeds')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS parsed_feeds (
                        parsed_feeds_id INTEGER PRIMARY KEY,
                        feed_id         INTEGER,
                        guid            TEXT UNIQUE)
                    ''')

                logging.debug(debug_info() + 'Created table:' + 'parsed_feeds')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS scripts (
                        script_id   INTEGER PRIMARY KEY,
                        feed_id     INTEGER,
                        script      BLOB,
                        options     BLOB)
                    ''')

                logging.debug(debug_info() + 'Created table' + 'feeds')

                connection.commit()

        except sqlite3.Error as e:
            logging.debug(debug_info() + str(e.args[0]))
            raise e

def get_available_scripts():
    available_scripts = []
    for i in dir(scripts):
        obj = eval('scripts.'+i)
        try:
            if obj is not scripts.Script and issubclass(obj, scripts.Script):
                available_scripts.append(obj)
        except TypeError:
            pass
    return available_scripts

def debug_info():
    return ':' + str(sys._getframe(1).f_code.co_filename) + ':' + \
        str(sys._getframe(1).f_code.co_name) + ':' + \
        str(sys._getframe(1).f_lineno) + ':'
