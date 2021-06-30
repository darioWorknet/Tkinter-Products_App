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

    def update_product(self, new_name, new_price, new_categorie, old_name, old_price, old_categorie):
        if new_name and new_price and old_name and old_price:
            old_id, = self.get_categorie_ID(old_categorie)
            new_id,= self.get_categorie_ID(new_categorie)
            query = 'UPDATE producto SET nombre = ?, precio = ?, categoriaID = ? WHERE nombre = ? AND precio = ? AND categoriaID = ?'
            self.db_query(query, new_name, new_price, new_id, old_name, old_price, old_id)
            return True
        return False

    def get_using_categorie_id(self):
        query = 'SELECT categoriaID FROM producto'
        result = self.db_query(query)
        unique_categorie_id = set()
        for r, in result:
            unique_categorie_id.add(r)
        return unique_categorie_id

    def get_all_categorie_id(self): 
        query = 'SELECT id FROM categoria'
        result = self.db_query(query)
        unique_id = set()
        for r, in result:
            unique_id.add(r)
        return unique_id
    
    def del_not_using_categories(self):
        all_ids = self.get_all_categorie_id()
        using_ids = self.get_using_categorie_id()
        ids_to_delete = [id for id in all_ids if id not in using_ids]
        for id in ids_to_delete:
            query = 'DELETE FROM categoria WHERE id = ?'
            self.db_query(query, id)




# Debugging
if __name__ == '__main__':
    # Inicializacion de la base de datos
    db = 'database/productos.db'
    db = DB(db)

    # res = db.get_categories()
    # print(res)

    # bol = db.item_in_table(table="categoria", col="nombre", item="Test")
    # print(bol)


    db.del_not_using_categories()


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