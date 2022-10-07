import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index( 'Fruit')


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🍲 Omega 3 & Blueberry Oatmeal')
streamlit.text('🧋 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚 Hard-Boiled Free-Range Egg')
streamlit.text('🥑 Avacado on Toast')

streamlit.header('🍓🍌 Build Your Own Breakfast Smoothie! 🍉🍇')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe (fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

def get_fruity_vice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruity_vice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  
# Load Fruit List
def get_fruit_load_list():
  with my_cnx.cursor as my_cur:
    my_cur.execute("SELECT fruit_name from fruit_load_list")
    my_data_rows = my_cur.fetchall()
    return my_data_rows
    
streamlit.header("The Fruit Load List contains:")

if streamlit.button('Load Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  #my_cnx.close()
  streamlit.dataframe(my_data_rows)
  
# Add new Fruit to List

add_my_fruit = streamlit.text_input('What fruit would you like to add:')
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list(fruit_name) values ('"+new_fruit+"')")
    return streamlit.write('Thanks for adding ', add_my_fruit)
    
if streamlit.button('Add a fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
 # my_cnx.close()
  


    



