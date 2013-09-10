#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['config', 'core', 'scripts']

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Session = scoped_session(sessionmaker())
engine = None
