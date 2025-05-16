import sqlite3
import csv

# Подключение к базе данных
conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

# SQL-запрос в соответствии с указанными шагами
query = """
SELECT a.name AS author_name, 
       p.year AS publish_year, 
       p.title AS paper_title, 
       p.pdf_name, 
       p.abstract AS paper_abstract, 
       p.paper_text
FROM papers AS p
INNER JOIN paper_authors AS pa ON p.id = pa.paper_id
INNER JOIN authors AS a ON pa.author_id = a.id;
"""

# Выполнение запроса
cursor.execute(query)
rows = cursor.fetchall()

# Экспорт в CSV
with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["author_name", "publish_year", "paper_title", "pdf_name", "paper_abstract", "paper_text"])
    writer.writerows(rows)

# Закрытие соединения
conn.close()

# fii