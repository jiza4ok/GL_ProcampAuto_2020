import sqlite3


class BaseSQLiteDB:
    """ Base class for working with SQLite3 database """

    def __new__(cls, attr):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_file: str):
        try:
            self.connection = sqlite3.connect(db_file)
        except Exception as exp:
            print(exp)
        self.cursor = self.connection.cursor()

    def destroy_connection(self):
        """ destroys connection with database """
        self.cursor.close()
        self.connection.close()

    def select_query(self, query: str, limit=50):
        """ executes a select query provided as an argument
            returns: a list of tuples with db data requested
        """
        self.cursor.execute(query)
        return self.cursor.fetchmany(size=limit)

    def update_query(self, query: str):
        """ executes an update query provided as an argument
            param: query as a string
        """
        self.cursor.execute(query)
        self.connection.commit()


if __name__ == '__main__':
    db = BaseSQLiteDB('database/kayaks_purchases.db')

    # some workflow code here
    # list of possible queries is available in Lecture_SQL/database/queries_for_kayaks_purchases_db.txt file
    # the database schema can be found in Lecture_SQL/database/kayaks_purchases_db(Schema).png

    db.destroy_connection()
