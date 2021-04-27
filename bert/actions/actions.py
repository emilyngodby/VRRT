# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import sqlite3
from sqlite3 import Error
import os

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
class ActionSubmit(Action):

    def name(self) -> Text:
        return "action_submit"

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
        specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        # if not os.path.exists(dbfile):
        #     os.makedirs(dbfile)
        #     os.system()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, db_file)

        conn = None
        try:
            conn = sqlite3.connect(db_path)
        except Error as e:
            print(e)

        return conn

    def create_project(self, conn, project):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO slots (pain, pain_location, missed_events, sleep, stress, feedback)
              VALUES(?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, project)
        conn.commit()
        return cur.lastrowid

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        database = r"rasa.db"

        conn = self.create_connection(database)

        sql_create_slots_table = """CREATE TABLE IF NOT EXISTS slots (
                                        pain varchar(32),
                                        pain_location varchar(32),
                                        missed_events varchar(32),
                                        sleep varchar(32),
                                        stress varchar(32),
                                        feedback varchar(32))"""

        if conn is not None:
            self.create_table(conn, sql_create_slots_table)
        
        with conn:
            slots =(tracker.get_slot("pain"),
                    tracker.get_slot("pain_location"),
                    tracker.get_slot("missed_events"),
                    tracker.get_slot("sleep"),
                    tracker.get_slot("stress"),
                    tracker.get_slot("feedback"))

            project_id = self.create_project(conn, slots)

        return []
