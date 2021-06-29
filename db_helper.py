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
        query = '''SELECT p.nombre, p.precio, c.nombre
        FROM producto as p 
        INNER JOIN categoria as c
        ON p.categoriaID = c.ID'''
        return self.db_query(query)

    def get_categorie_ID(self, categorie):
        query = f'SELECT id FROM categoria WHERE nombre = ?'
        result = self.db_query(query, categorie)
        return result.fetchall()[0]
  

    def get_categories(self):
        query = 'SELECT nombre FROM categoria ORDER BY nombre'
        result = self.db_query(query)
        return [x[0] for x in result]       

    def add_product(self, name, price, categorie):
        categorie_id, = self.get_categorie_ID(categorie)
        query = 'INSERT INTO producto VALUES (NULL, ?, ?, ?)'
        self.db_query(query, name, price, float(categorie_id))

    def item_in_table(self, table, col, item):
        query = f'SELECT {col} FROM {table}'
        result = self.db_query(query)
        for r, in result:
            if item == r:
                return True
        return False

    def add_categorie(self, categorie):
        if not self.item_in_table('categoria', 'nombre', categorie):
            query = 'INSERT INTO categoria VALUES (NULL, ?)'
            self.db_query(query, categorie)
            return True
        return False

    def del_product(self, product):
        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_query(query, product)

    def del_categorie(self, categorie):
        query = 'DELETE FROM categoria WHERE nombre = ?'
        self.db_query(query, categorie)

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

    res = db.get_categories()
    print(res)

    bol = db.item_in_table(table="categoria", col="nombre", item="Test")
    print(bol)


    # db.add_product("new", 111) # Añadir nuevo producto

    # db.del_product('new') # Borrar producto

    # db.update_product('asdddddd', 333, 'asd', 33) # Modificar producto

    # query = 'SELECT * FROM producto ORDER BY nombre DESC' # Imprimir tabla
    # result = db.get_products()
    # for row in result:
    #     print(row)

    # print(db.get_categories())

    # query =  '''SELECT p.nombre, p.precio, c.nombre
    #             FROM producto as p 
    #             INNER JOIN categoria as c
    #             ON p.categoriaID = c.ID'''

    # result = db.db_query(query)
    # for r in result:
    #     print(r)


    # query = 'SELECT id FROM categoria WHERE categoria = "Gaming"'
    # result = db.db_query(query)
    # # for r in result:
    # #     print(*r)
    # l = [x for x in result]
    # print(l)
    # id_ = db.get_categorie_ID("Gaming")
    # print(*id_)

    # db.del_categorie("Aeromodel")