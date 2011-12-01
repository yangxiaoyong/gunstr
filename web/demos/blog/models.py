# -*-encoding:utf-8 -*-

import time
import logging
import itertools
import sqlite3

class SqliteModel(object):
    def __init__(self, database, max_idle_time=7*3600, auto_commit=True):
        self.database = database

        self.max_idle_time = max_idle_time
        self._db = None
        self._last_use_time = time.time()

        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to sqlite, path: %s", self.database, exc_info=True)

        if auto_commit: self._db.isolation_level = None

    def __del__(self):
        self.close()

    def _ensure_connect(self):
        if (self._db is None or
                (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connect()
        return self._db.cursor()

    def _execute(self, cursor, query, parameters):
        try:
            return cursor.execute(query, parameters)
        except Exception:
            logging.error("Error connectiong to sqlite %s" % self.database, exc_info=True)
            self.close()
            raise

    def iter(self, query, *parameters):
        self._ensure_connect()
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names, row)) for row in cursor]
        finally:
            cursor.close()


    def execute(self, query, *parameters):
        """Executes the given query, returning the lastrowid from the query."""
        return self.execute_lastrowid(query, *parameters)

    def execute_lastrowid(self, query, *parameters):
        """Executes the given query, returing the lastrowid from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def close(self):
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        """Close the existing database connection and re-open it."""
        self.close()
        self._db = sqlite3.connect(self.database)
        self._last_use_time = time.time()

    def query(self, query, *parameters):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def get(self, query, *parameters):
        """Returns the first row returned for the given query."""
        rows = self.query(query, *parameters)
        if not rows:
            return None
        elif len(rows) > 1:
                raise Exception("Multiple rows returned for SqliteModel.get() query")
        return rows[0]

    def executescript(self, sql_file):
        with open(sql_file, 'rb') as fb:
            content = fb.read()
            cursor = self._cursor()
            cursor.executescript(content)

class Row(dict):
    """A dict that allows for object-like property access syntax"""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
