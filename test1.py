import sqlite3

db = sqlite3.connect('blog.db')
sql = db.cursor()
sql.execute (''' CREATE TABLE IF NOT EXISTS user_info(
  user_text TEXT, 
  user_title STRING,
  user_intro STRING
) ''')

db.commit()

text = input('Text: ')
title = input('Title: ')
intro = input("Intro: ")


sql.execute("SELECT user_text FROM user_info")
if sql.fetchone() is None:
  sql.execute(f"INSERT INTO user_info VALUES ('{text}', '{title}', '{intro}')")
  db.commit()
else:
  print("Такая запись существует")