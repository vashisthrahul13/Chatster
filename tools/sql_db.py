from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase	#sqlalchemy wrapper around database
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from sqlalchemy import create_engine,text

import re
import os
from dotenv import load_dotenv


# # Go one step back to the base folder
base_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "..",'..'))

# Construct the .env path
env_path = os.path.join(base_dir, ".env")

load_dotenv(env_path)

#----------- set DB URI ---------
DB_URI = "mysql+pymysql://root:password@localhost:3306/sql_practice"

#---------DB wrapper ------
db = SQLDatabase.from_uri(DB_URI)

#-------initialize llm-----
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0) #temp 0 to make model deterministic

# ------------------ 4. Toolkit & Agent ----------------
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# ------------------ 5. Prompt Template ----------------
sql_prompt = PromptTemplate(
    template="""
You are a MySQL expert. Convert the following natural language request into a valid MySQL query.
Return ONLY the SQL query, nothing else.

Question: {question}
SQL Query:
""",
 input_variables=["question"],
)


# ------------------ 6. Blocked Keywords ----------------
BLOCKED_KEYWORDS = ["DROP", "DELETE", "ALTER", "TRUNCATE", "UPDATE"]

@tool
def query_db(query:str)-> dict:
    """
    Query the MySQL database in natural language.
    Converts question -> SQL query -> validates -> executes safely.
    """

    try:
        parser = StrOutputParser()
        sql_query_chain = sql_prompt | llm | parser
        sql_query = sql_query_chain.invoke({'question':query})

        if any(keyword in sql_query.upper() for keyword in BLOCKED_KEYWORDS):
            return {
                "error": "Query contains unsafe operations. Allowed: SELECT, SHOW, DESCRIBE, etc.",
                "generated_sql": sql_query,
            }
        
        #excute safe query
         # 4. Execute safe query
        result = db.run(sql_query)

        return {
            "query": query,
            "generated_sql": sql_query,
            "response": result,
        }

    except Exception as e:
        return {"error": str(e)}
