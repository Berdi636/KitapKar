import psycopg2
from psycopg2 import Error
from typing import List, Union

connection = psycopg2.connect(
    user='postgres',
    database='users'
)


class DB():
    @staticmethod
    def execute(query: str, params: tuple):
        cursor = connection.cursor()

        try:
            cursor.execute(query, params)
            connection.commit()

        except (Exception, Error) as error:
            print(error)

        finally:
            cursor.close()

    @staticmethod
    def select_one(query: str, params: dict):
        cursor = connection.cursor()
        results: List = Union[None]  # type: ignore
        
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            # print(results)

        except (Exception, Error) as error:
            print(error)

        finally:
            cursor.close()
        
        
        return results  

    
    @staticmethod
    def select(query: str):
        cursor = connection.cursor()
        results: List[tuple] = []  
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            # print(results)

        except (Exception, Error) as error:
            print(error)

        finally:
            cursor.close()

        return results
        
