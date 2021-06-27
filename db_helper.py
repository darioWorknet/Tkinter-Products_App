import sqlite3


class DB:
    def __init__(self, db):
        self.db = db

    def db_query(self, query, *args):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, args)
            conn.commit()
        return result

    def get_products(self):
        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        return self.db_query(query)

    def add_product(self, name, price):
        query = 'INSERT INTO producto VALUES (NULL, ?, ?)'
        self.db_query(query, name, price)

    def del_product(self, product):
        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_query(query, product)

    def update_product(self, new_name, new_price, old_name, old_price):
        if new_name and new_price and old_name and old_price:
            query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
            self.db_query(query, new_name, new_price, old_name, old_price)
            return True
        return False


# Debugging
if __name__ == '__main__':
    # Inicializacion de la base de datos
    db = 'database/productos.db'
    db = DB(db)

    # db.add_product("new", 111) # Añadir nuevo producto

    # db.del_product('new') # Borrar producto

    db.update_product('asdddddd', 333, 'asd', 33) # Modificar producto

    query = 'SELECT * FROM producto ORDER BY nombre DESC' # Imprimir tabla
    result = db.get_products()
    for row in result:
        print(row)