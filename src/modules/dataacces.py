import psycopg2
import pandas as pd
from enum import Enum
import time

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SearchType(Enum):
    """ 
    Enum for search types for searcing source or destination columns in the lineage tables
    """
    SOURCE = 1
    DESTINATION = 2

class PostgreSQLClient:
    def __init__(self, host, port, database, user, password):
        """
        Initialize PostgreSQL client.
        """
        self.connection = None
        self.config = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password
        }
    
    # def _connect(self):
    #     """
    #     Establish connection to PostgreSQL database.
    #     """
    #     try:
    #         self.connection = psycopg2.connect(**self.config)
    #     except psycopg2.Error as e:
    #         print(f"Error connecting to PostgreSQL: {e}")
    #         raise

    def query_pipeline_to_pipeline(self, searchtype: SearchType=SearchType.SOURCE, conditions=None):
        """
        Query the pipelinetopipeline table under the lineage schema and return a pandas DataFrame.
        :param searchtype: Enum to specify whether to search source or destination columns           
        :param conditions: Optional WHERE clause as a dictionary {column: value}
        :return: pandas DataFrame with query results
        """
    
        query = 'select * from "Lineage".pipelinetopipeline'
        params = []
        if conditions:
            where_clauses = []
            for column, value in conditions.items():
                if '*' in value:
                    # Handle wildcard search
                    value = value.replace('*', '%')
                if '%' in value:
                    where_clauses.append(f"{column} LIKE %s")
                    params.append(value)
                else:
                    where_clauses.append(f"{column} = %s")
                    params.append(value)
            query += " WHERE " + " AND ".join(where_clauses)
            print(f"QUERY: {query}")

        try:
            start_time = time.time()
            with psycopg2.connect(**self.config) as dbconnection:
                connection_time= time.time() - start_time
                logging.info(f"Connected in {connection_time:.3f} seconds to PostgreSQL database:{self.config['database']} on {self.config['host']} at port {self.config['port']}")
                with dbconnection.cursor() as cursor:
                        logging.info(f"Executing query: {query} with params: {params}")
                        cursor.execute(query, params)
                
                        # Fetch column names
                        colnames = [desc[0] for desc in cursor.description]
                        
                        # Fetch data and convert to Pandas DataFrame
                        start_time= time.time()
                        df = pd.DataFrame(cursor.fetchall(), columns=colnames)
                        logging.info(f"Fetched {len(df)} rows in {time.time() - start_time:.3f} seconds")
            return df
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            logging.error(f"Error executing query: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on failure



if __name__=="__main__":
   
    # Example usage
    client = PostgreSQLClient(host="192.168.1.13", port=5432, database="mydatabase", user="myuser", password="mypassword")
    # Query with conditions
    conditions = {
        "sourcepipelineid":  "*pipe*1",
        "sourcetable": "table1"
        }   # Replace with actual column and value
    df_with_conditions = client.query_pipeline_to_pipeline(conditions=conditions)
    print(df_with_conditions)  # Print first few rows of the filtered DataFrame