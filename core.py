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

installedScripts = {
    'transmissionDaemonScript': scripts.transmissionDaemonScript
}

class Feed(Base):
    __tablename__ = 'Feeds'

    id = Column(Integer, primary_key=True)
    location = Column(String, unique=True)
    data = Column(PickleType)

    oldEntries = relationship(
        'OldEntry', backref="feed",
        cascade="all, delete, delete-orphan")
    scripts = relationship(
        'Script', backref="feed",
        cascade="all, delete, delete-orphan")

    def __init__(self, location, data):
        self.location = location        
        self.data = data
        Session.commit()

    def __repr__(self):
        return '<Feed({}, {})>'.\
            format(self.id, self.location)

    def attachScript(self, name, options):
        self.scripts.append(Script(name, options))
        Session.commit()

    def addOldGuid(self, guid):
        self.oldEntries.append(OldEntry(guid))
        Session.commit()

    def getAllOldGuids(self):
        oldGuids = []
        for oldEntry in self.oldEntries:
            oldGuids.append(oldEntry.guid)
        return oldGuids

    def setAllOld():
        for entry in self.data.entries:
            self.addOldGuid(entry.guid)

    def runAll(self):
        for script in self.scripts:
            script.run()
        self.setAllOld()
         
    def update(self):
        self.data = feedparser.parse(self.location)
        self.runAll()
        Session.commit()

class OldEntry(Base):
    __tablename__ = 'OldEntries'

    id = Column(Integer, primary_key=True)
    feedId = Column(Integer, ForeignKey(Feed.id))
    guid = Column(String, unique=True)

    def __init__(self, guid):
        self.guid = guid
        Session.commit()

    def __repr__(self):
        return '<OldEntry({}, {})>'.\
            format(self.feedId, self.guid)

class Script(Base):
    __tablename__ = 'Scripts'

    id = Column(Integer, primary_key=True)
    feedId = Column(Integer, ForeignKey(Feed.id))
    name = Column(String)
    options = relationship(
        'Option', cascade="all, delete, delete-orphan")

    def __init__(self, name, options):
        self.name = name
        self.setOptions(options) 
        Session.commit()

    def __repr__(self):
        return '<Script({}, {}, {}>'.\
            format(self.feedId, self.name, self.options)

    def getScript(self):
            return installedScripts[self.name]

    def setOptions(self, options):
        script = self.getScript()
        for key in options:
            if not key in script._default_options:
                raise KeyError
            self.options.append(Option(key, options[key]))             
        Session.commit()

    def getOptions(self):
        options = {}
        for option in self.options:
            options[option.name] = option.value
        return options

    def run(self):
        script = self.getScript()
        script.run(self.feed, self.getOptions())

class Option(Base):
    __tablename__ = 'Options'

    id = Column(Integer, primary_key=True)
    script_id = Column(Integer, ForeignKey(Script.id))
    name = Column(String)
    value = Column(String)

    def __init__(self, name, value):
        self.name = name
        self.value = value
        Session.commit()

    def __repr__(self):
        return '<Option({}={})>'.\
            format(self.name, self.value)

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
        Session.commit()

    def __len__(self):
        """ Return the number of feeds """
        return Session.query(Feed).count()

    def addFeed(self, location):
        """ Add a feed """
        data = feedparser.parse(location)
        Session.add(Feed(location, data))
        Session.commit()

    def getAllFeeds(self):
        """ Return a list of all the feeds """
        return Session.query(Feed).order_by(Feed.id).all()

    def getAllScripts(self):
        """ Get list of all scripts """
        return Session.query(Script).order_by(Script.id).all()

    def getAllOldEntries(self):
        """ Get list all the old entries """
        return Session.query(OldEntry).all()

    def getFeedById(self, feedId):
        """ Get the feed by its id """
        return Session.query(Feed).\
            filter(Feed.id==feedId).\
            one()

    def getScriptById(self, script_id):
        """ Get the script by its id """
        return Session.query(Script).\
            filter(Script.id == script_id).\
            one()

    def removeFeed(self, feed):
        """ Remove the feed from the database """
        Session.delete(feed)
        Session.commit()

    def removeFeedById(self, feedId):
        """ Remove the feed from the database """
        feed = self.getFeedById(feedId)
        self.removeFeed(feedId)

    def removeScript(self, script):
        Session.delete(script)
        Session.commit()

    def removeScriptById(self, scriptId):
        """ Remove the script from the database """
        script = self.getScriptById(scriptId)
        self.removeScript(script)

    def updateAll(self):
        """ update all feeds """
        for feed in self.feedsGetAll():
            feed.update()

def debug_info():
    return ':' + str(sys._getframe(1).f_code.co_filename) + ':' + \
        str(sys._getframe(1).f_code.co_name) + ':' + \
        str(sys._getframe(1).f_lineno) + ':'
