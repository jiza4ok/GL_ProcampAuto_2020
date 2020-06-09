import psycopg2

class Config:
    host = 'localhost'
    port = '5432'
    user = 'tester'
    password = 'tester'
    db = 'testDB'

class Queries:
    # Queries used just as example. Local test DB used for the task

    SELECT1 = 'SELECT * FROM public."testTable" LIMIT 10'
    SELECT2 = "SELECT * FROM public.\"testTable\" WHERE \"City\" = 'Boston'"

    UPDATE1 = "UPDATE public.\"testTable\" SET \"LastName\"='Cat' WHERE \"LastName\" = 'Mouse';"
    UPDATE2 = "UPDATE public.\"testTable\" SET \"LastName\"='Mouse' WHERE \"LastName\" = 'Cat';"

class DBConnection():
    # constructor creates connection to DB and cursor to operate with data(execute queries)
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        try:
            self.connection = psycopg2.connect(host=host, port=port, user=user, password=password, database=db)
            self.cursor = self.connection.cursor()  
        except:
            print('Cannot connect to te DB')

    # method used to execute SELECT queries, returns a list of tuples
    def select(self, selectQuery):
        try:
            self.cursor.execute(selectQuery)
            records = self.cursor.fetchall()
            return records
        except:
            print("Wrong SELECT query")

    # method used to execute SELECT queries, returns number of rows affected by the UPDATE statement
    def update(self, updateQuery):
        try:
            self.cursor.execute(updateQuery)
            updatedRowCount = self.cursor.rowcount
            return updatedRowCount
        except:
            print("Wrong UPDATE query")

    def commit(self):
        self.connection.commit()

    def destroy(self):
        self.cursor.close()
        self.connection.close()
