import oracledb

def get_connection():
    try:
        conn = oracledb.connect(
            user='xxxx', 
            password='xxxxx', 
            dsn='xxxxx'
        )
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco:", e)
        return None