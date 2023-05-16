import snowflake.connector
import pandas as pd
import streamlit as st

conn = snowflake.connector.connect(
    USER_NAME=st.secrets["USER_NAME"],
    PASSWORD=st.secrets["PASSWORD"],
    ACCOUNT=st.secrets["ACCOUNT"],
    WAREHOUSE=st.secrets["WAREHOUSE"],
    ROLE=st.secrets["ROLE"],
    DATABASE=st.secrets["DATABASE"],
    SCHEMA=st.secrets["SCHEMA"],
)


# Create a cursor object.
cur = conn.cursor()


# function - run sql query and return data
def query_data_warehouse(sql: str, parameters=None) -> any:
    """
    Executes snowflake sql query and returns result as data as dataframe.
    Example of parameters
    :param sql: sql query to be executed
    :param parameters: named parameters used in the sql query (defaulted as None)
    :return: dataframe
    """    
    if parameters is None:
        parameters = {}
    query = sql
    
    try:
        cur.execute("USE DATABASE " + st.secrets["DATABASE"])
        cur.execute("USE SCHEMA " + st.secrets["SCHEMA"])
        cur.execute(query, parameters)
        all_rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        
    except Exception as e:
        return e
    
    finally:
        print("closing cursor")

    df = pd.DataFrame(all_rows)
    df.columns = field_names
    return df
