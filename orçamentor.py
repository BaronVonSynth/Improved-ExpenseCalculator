#--Imports--#
import sqlite3 as lite
#--Dbstarter--#
con = lite.connect('dados.db')

#--Tabela Categoria--#
with con:
    mouse = con.cursor()
    mouse.execute('CREATE TABLE Categoria(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)')
#--Tabela Receita--#
with con:
    mouse = con.cursor()
    mouse.execute('CREATE TABLE Receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL)')
#--Tabela Gastos--#
with con:
    mouse = con.cursor()
    mouse.execute('CREATE TABLE Gastos (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)')

