# make_db.py generated by R. Yokoyama 10/04/2018
import sqlite3
import re

db = sqlite3.connect('db/nuclei.db')
# FRDM + HF statistical model by Moller
sql = "create table frdm_beoh(Z integer, N integer, A integer, P0n float, P1n float, P2n float, P3n float, P4n float, P5n float, P6n float, P7n float, P8n float, P9n float, P10n float, En_ float, n_ float, exp integer);"
db.execute(sql)
# FRDM by Moller
sql = "create table frdm_old(Z integer, N integer, E float, P0n float, P1n float, P2n float, P3n float);"
db.execute(sql)
# EDM by K. Miernik
sql = "create table edm(A integer, Z integer, P1n float, P2n float, P3n float);"
db.execute(sql)
# CDFT by T. Marketin
sql = "create table cdft(Zchar string, Z integer, N integer, A integer, LGT float, LFF float, LTot float, FFpTot float, halflife float, P0n float, P1n float, P2n float, P3n float, P4n float, P5n float, n_ float, E_e float, E_nu float, E_g float);"
db.execute(sql)

# loads from FRDM + HF
txt_file = open('txtdata/pn-frdm2012-sdn-gtff-beoh350.txt','r')
for line in txt_file:
    words = list(filter(None, re.split(' +', line)))
    if words[0].isdigit():
        sql = "insert into frdm_beoh values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        db.execute(sql, words)

txt_file.close()

# loads from FRDM
txt_file = open('txtdata/tpnff.dat','r')
for line in txt_file:
    words = list(filter(None, re.split('\s+', line)))
    sql = "insert into frdm_old values(?,?,?,?,?,?,?);"
    db.execute(sql, words)

# loads from EDM
txt_file = open('txtdata/predictions_multi.txt','r')
for line in txt_file:
    words = list(filter(None, re.split('\s+', line)))
    if words[0].isdigit():
        sql = "insert into edm values(?,?,?,?,?);"
        db.execute(sql, words)

# loads from CDFT
txt_file = open('txtdata/PRC-marketin.dat','r')
for line in txt_file:
    words = list(filter(None, re.split('\s+', line)))
    sql = "insert into cdft values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
    db.execute(sql, words)

sql = "alter table frdm_beoh add column halflife float;"
db.execute(sql)
sql = "alter table frdm_old add column halflife float;"
db.execute(sql)
sql = "alter table edm add column P0n integer;"
db.execute(sql)
sql = "alter table edm add column N integer;"
db.execute(sql)
sql = "alter table edm add column halflife float;"
db.execute(sql)

# add N and P0n columns to EDM
cursor = db.cursor()
sql = "select * from edm"
cursor.execute(sql)
for row in cursor:
    sql = "update edm set N = " + str(row[0]-row[1]) + " where A = " + str(row[0]) + " AND Z = " + str(row[1])
    db.execute(sql)
    sql = "update edm set P0n = " + str(1.0 - row[2] - row[3] - row[4]) + " where A = " + str(row[0]) + " AND Z = " + str(row[1])
    db.execute(sql)

db.commit()

# loads Half-life data
txt_file = open('txtdata/tlifminusff-beta-2018.dat','r')
for line in txt_file:
    words = list(filter(None, re.split(' +', line)))
    sql = "update frdm_beoh set halflife = " + words[2] + " where Z = " + words[0] + " AND N = " + words[1]
    db.execute(sql)
    sql = "update frdm_old set halflife = " + words[2] + " where Z = " + words[0] + " AND N = " + words[1]
    db.execute(sql)
    sql = "update edm set halflife = " + words[2] + " where Z = " + words[0] + " AND N = " + words[1]
    db.execute(sql)
    
txt_file.close()

db.commit()
db.close()
