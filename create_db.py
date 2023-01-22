import sqlite3
import pandas as pd

columnnames='''Sijainti text,
Kaupunginosa text,
link text,
Kerros text,
Asuinpinta_ala text,
Huoneiston_kokoonpano text,
Huoneita text,
Kunto text,
Parveke text,
Velaton_hinta real,
Myyntihinta real,
Neliohinta real,
Rahoitusvastike text,
Hoitovastike text,
Yhtiovastike real,
Hoitovastike_m2 real,
Rakennuksen_tyyppi text,
Rakennusvuosi text,
Rakennusmateriaali text,
Energialuokka text,
Tontin_omistus text,
Kerroksia text,
Hissi text,
Asumistyyppi text,
Asunnossa_sauna text,
pvm text,
id text,
status text,
myyntikesto text'''

columnnames_aggregates='''metric text,
Kerros real,	
Asuinpinta_ala real,
Huoneita real,	
Velaton_hinta real,	
Myyntihinta real,	
Neliohinta real,	
Rahoitusvastike real,	
Hoitovastike real,	
Yhtiovastike real,	
Rakennusvuosi real,	
Kerroksia real,	
Hoitovastike_m2 real'''

conn=sqlite3.connect('oikotie.db')
c=conn.cursor()
##c.execute('''drop table if exists asunnot''')
c.execute('''drop table if exists asunnot_history''')
c.execute(f''' CREATE TABLE IF NOT EXISTS oikotie_asunnot({columnnames}) ''')
c.execute(f''' CREATE TABLE IF NOT EXISTS stg_oikotie_asunnot({columnnames}) ''')

c.execute(f''' CREATE TABLE IF NOT EXISTS asunnot_history({columnnames_aggregates}) ''')
##c.execute(f''' CREATE TABLE IF NOT EXISTS stg_asunnot({columnnames}) ''')

conn.commit()
conn.close()








