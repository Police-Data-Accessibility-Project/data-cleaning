"""
Manages operations involving database

"""
from sqlalchemy import create_engine, text
import polars as pl


class DatabaseManager:

    def __init__(self):
        # Initialize database connection to data_correction.db
        self.engine = create_engine('sqlite:///instance/data_correction.db')
        self.connection = self.engine.connect()

    def close(self):
        self.connection.close()
        self.engine.dispose()

    def reset_database(self):
        """
        Resets the database
        :return:
        """
        self.connection.execute(text('''
            DROP TABLE IF EXISTS agencies
        '''))
        self.connection.commit()
        self.create_table()

    def create_table(self):
        """
        Creates table in the database
        Table is named 'entries_to_validate' and structured as follows:
        - id (primary key)
        - name
        - state
        - url
        - proposed_url
        - reviewed (boolean)

        """
        self.connection.execute(text('''
        CREATE TABLE IF NOT EXISTS agencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            state VARCHAR(255),
            old_url VARCHAR(255),
            possible_correct_url VARCHAR(255),
            airtable_uid VARCHAR(255),
            submitted_name VARCHAR(255),
            no_web_presence BOOLEAN,
            rejection_reason VARCHAR(255),
            approved BOOLEAN
        );
        '''.strip()))
        self.connection.commit()


    def insert_initial_data(self, entries: list[dict]):
        """
        Insert initial data into the database
        :param entries: List of dictionaries where each dictionary represents a row
        :return:
        """
        for entry in entries:
            self.connection.execute(text(f'''
                INSERT INTO agencies (
                    name, 
                    state, 
                    old_url, 
                    possible_correct_url, 
                    airtable_uid, 
                    submitted_name, 
                    no_web_presence, 
                    rejection_reason, 
                    approved
                )
                VALUES (
                    :name, 
                    :state, 
                    :old_url, 
                    :possible_correct_url, 
                    :airtable_uid, 
                    :submitted_name, 
                    :no_web_presence, 
                    :rejection_reason, 
                    :approved
                )
            '''), entry)
        self.connection.commit()

    def get_entries_without_proposed_url(self) -> list[dict]:
        """
        Get entries that have not been reviewed
        :return:
        """
        result = self.connection.execute(text('''
            SELECT * FROM agencies WHERE possible_correct_url = ''
        '''))
        list_of_tuples = result.fetchall()
        # Convert list of tuples to list of dictionaries
        list_of_dicts = []
        for item in list_of_tuples:
            list_of_dicts.append({
                'id': item[0],
                'name': item[1],
                'state': item[2],
                'old_url': item[3],
                'possible_correct_url': item[4],
                'reviewed': item[5]
            })
        return list_of_dicts


    def update_entry(self, id: int, proposed_url: str):
        """
        Update entry with proposed url
        :param id:
        :param proposed_url:
        :return:
        """
        self.connection.execute(text('''
            UPDATE agencies
            SET possible_correct_url = :proposed_url
            WHERE id = :id
        '''), {'id': id, 'proposed_url': proposed_url})
        self.connection.commit()

    def get_completed_entries(self):
        """
        Get entries that have been reviewed
        :return:
        """
        result = self.connection.execute(text('''
            SELECT 
            airtable_uid,
            submitted_name,
            possible_correct_url,
            approved,
            rejection_reason
             FROM agencies WHERE 
            possible_correct_url != ''
            and approved = 1
        '''))
        list_of_tuples = result.fetchall()
        # Convert list of tuples to list of dictionaries
        list_of_dicts = []
        for item in list_of_tuples:
            list_of_dicts.append({
                'airtable_uid': item[0],
                'submitted_name': item[1],
                'homepage_url': item[2],
                'approved': 'checked' if item[3] == 1 else 'unchecked',
                'no_web_presence': 'unchecked',
                'rejection_reason': item[4],
            })
        return list_of_dicts
