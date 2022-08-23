import pyodbc

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-5JRMGN0\SQLEXPRESS;DATABASE=Cuotas_web;UID=sa;PWD=24681012')
cursor = cnxn.cursor()
