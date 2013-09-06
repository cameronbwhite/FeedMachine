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
from sqlalchemy import Column, Integer, String, PickleType
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Session = scoped_session(sessionmaker())
engine = None

class Feed(Base):
    __tablename__ = 'Feeds'

    id = Column(Integer, primary_key=True)
    location = Column(String)
    data = Column(PickleType)

    oldEntries = relationship('OldEntry')
    scripts = relationship('Script')

    def __init__(self, location, data):
        self.location = location        
        self.data = data

    def __repr__(self):
        return '<Feed({}, {})>'.\
            format(self.id, self.location)

    def update(self):
        self.data = feedparser.parse(self.location)
        Session.commit()

    def attachScript(self, script):
        self.scripts.append(script)
        Session.commit()

    def getAllOldGuids(self):
        oldGuids = []
        for oldEntry in self.oldEntries:
            oldGuids.append(oldEntry.guid)
        return oldGuids

    def addOldGuid(self, guid):
        self.oldEntries.append(OldEntry(guid))
        Session.commit()

class OldEntry(Base):
    __tablename__ = 'OldEntries'

    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey(Feed.id))
    guid = Column(String)

    def __init__(self, guid):
        self.guid = guid

    def __repr__(self):
        return '<OldEntry({}, {})>'.\
            format(self.feed_id, self.guid)

class Script(Base):
    __tablename__ = 'Scripts'

    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey(Feed.id))
    script = Column(PickleType)
    options = Column(PickleType)

    def __init__(self, script, options):
        self.script = script
        self.options = options

    def __repr__(self):
        return '<Script({}, {}, {}>'.\
            format(self.feed_id, self.script, self.options)

class FeedDB(object):
    """Summary of class

    Attributes:
        _database_filename:

    """

    def __init__(self, database_filename):
        """ Summary of __init__

        Args:
            database_filename: Filename of SQL database.
        """
        global engine
        self._database_filename = database_filename
        engine = create_engine(
            'sqlite:///{}'.format(self._database_filename))
        Session.configure(bind=engine, autoflush=False, expire_on_commit=False)
        Base.metadata.create_all(engine)

    def __len__(self):
        """ Return the number of feeds """
        return Session.query(Feed).count()

    def addFeed(self, location):
        """ Add a feed """
        data = feedparser.parse(location)
        Session.add(Feed(location, data))
        Session.commit()

    def getFeedById(self, feed_id):
        """ Get the feed by id """
        return Session.query(Feed).\
            filter(Feed.id==feed_id).\
            one()

    def getAllFeeds(self):
        """ Return a list of all the feeds. """
        return Session.query(Feed).order_by(Feed.id).all()

    def scriptGetById(self, script_id):
        return Session.query(Script).\
            filter(Script.id == script_id).\
            one()

    def getAllScripts(self):
        """ Get all scripts

        Returns:
            List of all the scripts
        """
        return Session.query(Script).order_by(Script.id).all()

    def getAllOldEntries(self):
        """ get a list all the old entries """
        return Session.query(OldEntry).all()

    def updateAll(self):
        """ update all feeds """
        for feed in self.feedsGetAll():
            feed.update()
            self.feedRunAll(feed_id)
        Session.commit()

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
