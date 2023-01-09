import mysql.connector


class Database(object):
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            password='apdlvmf4@@',
            user='root',
            database='PortfolioManager',
            use_pure=True
        )
        self.conn.set_charset_collation('utf8', 'utf8_general_ci')

