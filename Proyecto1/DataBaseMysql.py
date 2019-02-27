import pymysql
class DBClass:
    host=""
    user=""
    passwd=""
    database=""
    db = None
    cursor = None

    def __init__(self,host,user,passwd,database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        try:
            self.db = pymysql.connect(self.host,self.user,self.passwd,self.database)
            self.cursor = self.db.cursor()
        except Exception:
            print("Fallo la conexion con la base de datos")
    
    def closeConnection(self):
        self.cursor.close()
        self.db.close()
    
    def executeSelect(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def insertUpdateDelete(self,query):
        self.cursor.execute(query)
        self.db.commit()