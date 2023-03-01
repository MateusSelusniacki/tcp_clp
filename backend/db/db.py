import sqlite3
import hashlib
from os.path import exists


class db():
    def __init__(self):
        if(not exists('.\\tupy.db')):
            self.create_passwordtable()
            self.create_iptable()
            self.create_configuration_table()

    def create_passwordtable(self):
        con = sqlite3.connect(".\\tupy.db")
        password = "tupyMaster"
        
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE senha(
            senha text    
        )""")

        encrypted_password = self.encrypt(password)
        cursor.execute("INSERT INTO senha VALUES(?)",(encrypted_password,))

        con.commit()
        con.close()

    def create_iptable(self):
        con = sqlite3.connect(".\\tupy.db")
        ip = "127.0.0.1"
        port = 53123
        
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE ip(
            ip text,
            port integer    
        )""")

        cursor.execute("INSERT INTO ip VALUES(?,?)",(ip,port))

        con.commit()
        con.close()
    
    def create_configuration_table(self):
        con = sqlite3.connect(".\\tupy.db")
        
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE config(
            inicio integer,
            fim integer,
            recipe integer   
        )""")

        con.commit()
        con.close()

        for i in range(5):
            self.insert_config(7*i+1,7*i+7,i)

    def encrypt(self,string):
        return hashlib.sha384(string.encode()).hexdigest()

    def get_password(self):
        con = sqlite3.connect(".\\tupy.db")
        cursor = con.cursor()

        cursor.execute("""
            SELECT * FROM senha
        """)
        
        row = cursor.fetchone()

        con.commit()
        con.close()
        return row[0]

    def update_password(self,newPassword):
        con = sqlite3.connect(".\\tupy.db")
        cursor = con.cursor()

        encrypted_password = self.encrypt(newPassword)
        actual_password = self.get_password()

        cursor.execute("UPDATE senha SET senha=:newPassword WHERE\
            senha=:oldPassword",{'newPassword':encrypted_password,'oldPassword':actual_password})
        
        con.commit()
        con.close()

    def check_password(self,password):
        con = sqlite3.connect(".\\tupy.db")
        cursor = con.cursor()

        encrypted_password = self.encrypt(password)
        db_password = self.get_password()

        return encrypted_password == db_password


    def update_ip(self,oldip,newip,newport):
        con = sqlite3.connect(".\\tupy.db")
        cursor = con.cursor()

        cursor.execute("""UPDATE ip SET ip=:newip, port=:newport WHERE\
            ip=:oldip""",{'newip':newip,'newport':newport,'oldip':oldip})
        
        con.commit()
        con.close()
    
    def get_ip(self):
        con = sqlite3.connect(".\\tupy.db")
        cursor = con.cursor()

        cursor.execute("""
            SELECT * FROM ip
        """)
        
        row = cursor.fetchone()

        con.commit()
        con.close()
        return row

    
    def insert_config(self,inicio: int, fim: int,recipe: int):
        print(f'inserting {inicio} {fim}')
        try:
            int(inicio)
            int(fim)
        except:
            return False
        # Conecta ao banco de dados
        conn = sqlite3.connect('tupy.db')
        
        # Cria um cursor
        cursor = conn.cursor()
        
        # Insere os dados na tabela config
        cursor.execute('INSERT INTO config (inicio, fim, recipe) VALUES (?, ?, ?)', (inicio, fim,recipe))
        
        # Confirma a inserção dos dados
        conn.commit()
        
        # Fecha a conexão com o banco de dados
        conn.close()
        return True
    
    def get_all_config(self):
        con = sqlite3.connect(".\\tupy.db")
        cursor = con.cursor()

        cursor.execute("""
            SELECT * FROM config
        """)
        
        rows = cursor.fetchall()

        con.commit()
        con.close()
        return rows

    def delete_all_config(self):
        # Estabelece conexão com o banco de dados
        conn = sqlite3.connect('tupy.db')

        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Executa o comando SQL para excluir todos os dados da tabela especificada
        cursor.execute(f"DELETE FROM config")

        # Confirma a transação e fecha a conexão
        conn.commit()
        conn.close()

if(__name__ == '__main__'):
    database = db()