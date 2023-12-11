import psycopg2

HOST = "localhost"
DB_NAME = "COMP3005 Project"
USER = "postgres"
PASSWORD = "password"
PORT = 5432

class DBClient:
    def __init__(self):
        self._host = HOST
        self._dbname = DB_NAME
        self._user = USER
        self._password = PASSWORD
        self._port = PORT

    def _get_connection(self):
        # Return a new postgres connection
        return psycopg2.connect(host=self._host, dbname=self._dbname, user=self._user, password=self._password, port=self._port)

    def insert(self, query: str) -> tuple[int, str]:
        connection = self._get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query)
        except psycopg2.errors.UniqueViolation:
            return 400, "UniqueViolation"
        
        connection.commit()
        cursor.close()
        connection.close()

        return 200, "Success"

    def get(self, query: str) -> tuple[int, tuple]:
        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.execute(query)
        
        result = tuple(cursor.fetchall())
        
        connection.commit()
        cursor.close()
        connection.close()

        return 200, result
    
    def delete(self, query: str) -> tuple[int, str]:
        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.execute(query)
    
        connection.commit()
        cursor.close()
        connection.close()

        return 200, "Success"

