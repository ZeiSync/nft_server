import psycopg2

class DB:
    def __del__(self):
        self.db.close()

    def __init__(self):
        self.db = psycopg2.connect(
            database="instamint", 
            user='postgres',
            password='postgres', 
            host='127.0.0.1', 
            port= '5432'
        )
        print(" * Started database connection")
    
    def init_tables(self):
        cursor = self.db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS asset (contract_type text, owner text, hash text, metadata_url text)")
        cursor.execute("CREATE TABLE IF NOT EXISTS transaction (txid text, status text)")
        self.db.commit()
        cursor.close()

    def insert_asset(self, data):
        cursor = self.db.cursor()
        cursor.execute("""INSERT INTO asset (contract_type, owner, hash, metadata_url) VALUES (%s, %s, %s, %s)""", data)
        self.db.commit()
        cursor.close()
    
    def insert_transaction(self, data):
        cursor = self.db.cursor()
        cursor.execute("""INSERT INTO transaction (txid, status) VALUES (%s, %s)""", data)
        self.db.commit()
        cursor.close()
        
    def update_transaction_status(self, txid, status):
        cursor = self.db.cursor()
        cursor.execute(f"UPDATE transaction SET status = '{status}' WHERE txid = '{txid}'")
        self.db.commit()
        cursor.close()