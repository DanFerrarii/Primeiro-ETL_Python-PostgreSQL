import psycopg2

class Conector_postgres:

    def __init__ (self, host, db, user, password):
        try:
            self.host = host
            self.db = db
            self.user = user
            self.password = password
        except Exception as e:
            print(str(e))
            
    def conectar (self):
        '''Conecta no BD'''
        try:
            conn = psycopg2.connect( host=self.host, database=self.db, user=self.user, password=self.password)
            cursor = conn.cursor()
            return conn, cursor
        except Exception as e:
            print(str(e))
            
    def desconectar(self, conn, cursor):
        '''Desconecta do BD'''
        try:
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(str(e))
    
    def inserir(self, query):
        '''Inseri informações no BD'''
        try:
            conn, cursor = self.conectar()
            cursor.execute(query)
            self.desconectar(conn, cursor)
        except Exception as e:
            print(str(e))
            
    def selecionar(self, query):
        '''Seleciona informações do BD'''
        try:
            conn, cursor = self.conectar()
            cursor.execute(query)
            dados = cursor.fetchall()
            self.desconectar(conn, cursor)
            lista_dados = []
            for dado in dados:
                lista_dados.append(dado)
            return lista_dados
        except Exception as e:
            print(str(e))