import psycopg2 as pg
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


class Restorani:
    def __init__(self):
        self.con=pg.connect(
                database='Restoran',
                password='Yoyoba22',
                host='localhost',
                user='postgres',
                port='5432')
        self.upit = None
        self.porudzbina=None
        self.novaporudzbina=None
        self.jelo_restorani=None
    

    def get_porudzbina(self):
        self.porudzbina=pd.read_sql_query('''SELECT p.br_porudzbine, p.ime_prezime,p.adresa,p.datum_porudzbine,p.id_jela,p.id_restoran,j.cena 
                                            FROM Porudzbina p, Jelovnici j 
                                            WHERE p.id_jela = j.id_jela 
                                            ORDER BY br_porudzbine''',self.con)
    
    def lista_listbox(self):
        if self.porudzbina is None:
            self.get_porudzbina()

        b_br_porudzbine = self.porudzbina.iloc[:,0]
        b_datum_porudzbine = self.porudzbina.iloc[:,3]
        b_cena=self.porudzbina.iloc[:,6]
        b = b_br_porudzbine.astype('string') + '-' + b_datum_porudzbine.astype('string')+ '-' + b_cena.astype('string')

        return b.tolist()

    
    def lista_racun(self, br_porudzbine, datum_porudzbine, cena):
        if self.porudzbina is None:
            self.get_porudzbina()
        lr = '##############'+'\nBroj Porudzbine: ' + str(br_porudzbine) + '\nDatum: ' + str(datum_porudzbine) + '\nIznos: ' + str(cena) + ' RSD\n###############'
        with open('racun-{}.txt'.format(br_porudzbine), 'w') as file:
            file.write(lr)
    
    def nova_porudzbina(self, ime_prezime, adresa, datum_porudzbine, id_jela, id_restorana):
        cursor = self.con.cursor()
        br_porudzbine = int(self.porudzbina.iloc[-1, 0]) + 1 if len(self.porudzbina) > 0 else 1
        query = "INSERT INTO Porudzbina (br_porudzbine, ime_prezime, adresa, datum_porudzbine, id_jela, id_restoran) VALUES (%s, %s, %s, %s, %s, %s)"
        vrednosti = (br_porudzbine, ime_prezime, adresa, datum_porudzbine, id_jela, id_restorana)
        cursor.execute(query, vrednosti)
        self.con.commit()
        cursor.close()
        self.get_porudzbina()


    def get_jelo_restran(self):
        self.jelo_restorani = pd.read_sql_query(
            'SELECT r.naziv_restorana,j.jelo,j.cena,j.id_jela,r.id_restoran FROM Restorani r, Jelovnici j WHERE r.id_restoran=j.id_restoran',
            self.con
        )
        self.jelo_restorani['jelo_restorani'] = self.jelo_restorani.apply(
            lambda row: f"{row['naziv_restorana']}-{row['jelo']}-{row['cena']}-{row['id_jela']}-{row['id_restoran']}",
            axis=1
        )


    def lista_listbox1(self):
        if self.jelo_restorani is None:
            self.get_jelo_restran()
        return self.jelo_restorani['jelo_restorani'].tolist()


    def get_sql(self, query):
        self.upit = pd.read_sql_query(query, self.con)

    def export_excel(self, naziv_fajla, kolone):
        self.upit.to_excel(naziv_fajla, index=False)

        
    def jela_piechart(self, mesec):
        query = """
        SELECT j.jelo, COUNT(*) AS count
        FROM Jelovnici j
        JOIN Porudzbina p ON p.id_jela = j.id_jela
        WHERE EXTRACT(MONTH FROM p.datum_porudzbine) = %s
        GROUP BY j.jelo
        ORDER BY count DESC
        LIMIT 5;
        """
        result = pd.read_sql_query(query, self.con, params=[mesec])
        print(result)

        plt.figure(figsize=(6, 6))
        plt.pie(result['count'], labels=result['jelo'], autopct='%1.1f%%')
        plt.title(f"Top 5 jela - Mesec {mesec}")
        plt.show()
    
    def br_porudzbina(self,mesec):
        query="""
        SELECT r.naziv_restorana, COUNT(p.br_porudzbine) AS count
        FROM Restorani r
        JOIN Porudzbina p ON r.id_restoran=p.id_restoran
        WHERE EXTRACT(MONTH FROM p.datum_porudzbine) = %s
        GROUP BY r.naziv_restorana
        ORDER BY count DESC;
        """
        result = pd.read_sql_query(query, self.con,params=[mesec])
        print(result)
        
        plt.figure(figsize=(6, 6))
        plt.subplot(1,1,1)
        plt.bar(result['naziv_restorana'],result['count'],width=0.8)
        plt.title(f'Broj Porudzbina po Restoranu - Mesec {mesec}')
        plt.show()


R = Restorani()
R.get_porudzbina()
R.get_jelo_restran()
R.lista_listbox()
