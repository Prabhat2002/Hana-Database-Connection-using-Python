
#load .env file
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
load_dotenv()

os.environ["db_user"] = os.getenv("db_user")
os.environ["db_password"] = os.getenv("db_password")
os.environ["db_host"] = os.getenv("db_host")
os.environ["db_port"] = os.getenv("db_port")
os.environ["db_name"] = os.getenv("db_name")

connection_url = URL.create(
	drivername="hana",
    database=os.getenv('db_name'),
	username=os.getenv('db_user'),
	password=os.getenv('db_password'),
	host=os.getenv('db_host'),
	port=os.getenv('db_port')
)
db = create_engine(connection_url)

#what if I want to do it using connection string instead of URL object
connection_string = f"hana://{os.getenv('db_user')}:{os.getenv('db_password')}@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_name')}"
db = create_engine(connection_string)   

#test connection
try:
	from sqlalchemy import text, exc
	with db.connect() as connection:
		try:
			result = connection.execute(text("SELECT * FROM INVOICES"))
			print(result.fetchone())
		except exc.ProgrammingError as pe:
			print("Table 'INVOICES' does not exist or you do not have permission to access it.")
			print(f"Details: {pe}")
		except Exception as e:
			print(f"An error occurred while executing the query: {e}")
except Exception as e:
	print(f"Error connecting to the database: {e}")
 
#Print results using streamlit
import streamlit as st
st.title("HDB Connection Test")


# Convert into dataframe and display the results (existing)
import pandas as pd
df = pd.DataFrame(result.fetchall(), columns=result.keys())
print(df)
st.dataframe(df)

   

# somebody was writing db = sqldatabase.from_uri(connection_string) but it is giving error because there is no sqldatabase module in sqlalchemy. It should be create_engine instead of from_uri.
# db = sqldatabase.from_uri(connection_string) --- IGNORE --- 
# Can I do in this way using from_uri method?
# No, there is no from_uri method in sqlalchemy. You should use create_engine to create a connection to the database using the connection string. The from_uri method is not available in sqlalchemy, it is used in some other libraries like SQLAlchemy-Utils but not in the core SQLAlchemy library. So you should stick to using create_engine with the connection string to establish a connection to your HDB database.
# How otherone is able to do that using from_uri? 