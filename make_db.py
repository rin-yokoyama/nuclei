import sqlite3
import re

db = sqlite3.connect('db/nuclei.db')
sql = "create table frdm_beoh(Z integer, N integer, A integer, P0n float, P1n float, P2n float, P3n float, P4n float, P5n float, P6n float, P7n float, P8n float, P9n float, P10n float, En_ float, n_ float, exp integer);"
db.execute(sql)
sql = "create table frdm_old(Z integer, N integer, E float, P0n float, P1n float, P2n float, P3n float);"
db.execute(sql)

txt_file = open('txtdata/pn-frdm2012-sdn-gtff-beoh350.txt','r')
for line in txt_file:
    words = list(filter(None, re.split(' +', line)))
    if words[0].isdigit():
        sql = "insert into frdm_beoh values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        db.execute(sql, words)

txt_file.close()

txt_file = open('txtdata/tpnff.dat','r')
for line in txt_file:
    words = list(filter(None, re.split('\s+', line)))
    sql = "insert into frdm_old values(?,?,?,?,?,?,?);"
    db.execute(sql, words)

sql = "alter table frdm_beoh add column halflife float;"
db.execute(sql)
sql = "alter table frdm_old add column halflife float;"
db.execute(sql)

txt_file = open('txtdata/tlifminusff-beta-2018.dat','r')
for line in txt_file:
    words = list(filter(None, re.split(' +', line)))
    sql = "update frdm_beoh set halflife = " + words[2] + " where Z = " + words[0] + " AND N = " + words[1]
    db.execute(sql)
    
txt_file.close()
db.commit()
db.close()
