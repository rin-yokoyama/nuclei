import sqlite3
import re
from Nuclide import NuclideProperty

class NuclideGenerator:
    # generator class for NuclideProperty objects
    # generateNuclides returns a list of Nuclide objects
    # from the table [table_name] in the database [db_file]

    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def generateNuclides(self, table_name):
        # get list of Pxn columns
        sql = "select * from " + table_name
        self.cursor.execute(sql)
        names = list(map(lambda x: x[0], self.cursor.description))
        pn_names = []
        for name in names:
            if re.match('P.n',name):
                pn_names.append(name)

        self.cursor.row_factory = sqlite3.Row
        sql = "select * from " + table_name
        nuclList = []
        for row in self.cursor.execute(sql):
           nuclide = NuclideProperty()
           nuclide.n = row["N"]
           nuclide.z = row["Z"]
           pn = []
           for pn_name in pn_names:
               pn.append(row[pn_name])
           nuclide.pn = pn
           nuclide.halflife = row["halflife"]
           nuclList.append(nuclide) 
        return nuclList
