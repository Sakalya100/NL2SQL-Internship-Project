import re
import openai
import mysql.connector
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key = "")

mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

cursor = mydb.cursor()

def get_initial_message():
    messages=[
            {"role": "system", "content": "Given the following SQL tables, your job is to write queries given a user's request.\n \n  CREATE TABLE Customers (\n  CustomerID INT PRIMARY KEY, \n FirstName VARCHAR(50), \n LastName VARCHAR(50), \n     Email VARCHAR(100) UNIQUE,\n   Phone VARCHAR(15)); \n \n CREATE TABLE Orders (\n OrderID INT PRIMARY KEY,\n CustomerID INT,\n OrderDate DATE,\n TotalAmount DECIMAL(10, 2),\n FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)); \n \n  CREATE TABLE OrderDetails (\n OrderDetailID INT PRIMARY KEY,\n OrderID INT,\n ProductName VARCHAR(50),\n Quantity INT,\n Price DECIMAL(8, 2),\n FOREIGN KEY (OrderID) REFERENCES Orders(OrderID));"},
            {"role": "user", "content": "I want to learn about my data"},
            {"role": "assistant", "content": "Thats awesome, what do you want to know?"}
        ]
    return messages

def get_chatgpt_response(messages, inputs):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "Given the following SQL tables, your job is to write queries given a user's request.\n \n  CREATE TABLE Customers (\n  CustomerID INT PRIMARY KEY, \n FirstName VARCHAR(50), \n LastName VARCHAR(50), \n     Email VARCHAR(100) UNIQUE,\n   Phone VARCHAR(15)); \n \n CREATE TABLE Orders (\n OrderID INT PRIMARY KEY,\n CustomerID INT,\n OrderDate DATE,\n TotalAmount DECIMAL(10, 2),\n FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)); \n \n  CREATE TABLE OrderDetails (\n OrderDetailID INT PRIMARY KEY,\n OrderID INT,\n ProductName VARCHAR(50),\n Quantity INT,\n Price DECIMAL(8, 2),\n FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)); "
            },
            {
            "role": "user",
            "content": inputs
            }
        ],
        temperature=0.7,
        max_tokens=256,
        top_p=1
        )
    res = ""
    ans = response.choices[0].message.content
    sql_query = get_query(ans)
    cursor.execute(sql_query)
    for i in cursor:
        res+= str(i)
    return {"generated query":ans , "Result": res}


def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


def get_query(text):
# The text from ChatCompletionMessage
    message_text = text

    # Define a regular expression pattern to match SQL queries
    sql_query_pattern = re.compile(r'SELECT.*?;', re.DOTALL)

    # Find the first match in the text
    match = sql_query_pattern.search(message_text)

    # Extract the matched SQL query
    if match:
        sql_query = match.group()
        return sql_query
    else:
        return -1

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ str(st.session_state['responses'][i+1]) + "\n"
    return conversation_string