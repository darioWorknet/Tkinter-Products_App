import sqlite3


class DB:
    def __init__(self, db):
        self.db = db

    # Metodo generico para ejecutar querys. Recibe la query en forma de string y los parametros que utiliza la query
    def db_query(self, query, *args):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, args)
            conn.commit()
        return result

    # METODOS DE LECTURA ---------------------------------------------------------------------------------------------
    def get_products(self): # Selecciona el nombre, precio y categoria de cada producto. Es necesario un inner join.
        query = ''' SELECT p.nombre, p.precio, c.nombre
                    FROM producto as p 
                    INNER JOIN categoria as c
                    ON p.categoriaID = c.ID'''
        return self.db_query(query)

    def get_categorie_ID(self, categorie): 
        query = f'SELECT id FROM categoria WHERE nombre = ?'
        result = self.db_query(query, categorie)
        return result.fetchall()[0]

    def get_categories(self): # Obtenemos los nombres de todas las categorias
        query = 'SELECT nombre FROM categoria ORDER BY nombre'
        result = self.db_query(query)
        return [x[0] for x in result]

    def get_using_categorie_id(self): # Devuelve el id de las categorias que se encuentran en uso, por la tabla producto
        query = 'SELECT categoriaID FROM producto'
        result = self.db_query(query)
        unique_categorie_id = set()
        for r, in result:
            unique_categorie_id.add(r)
        return unique_categorie_id

    def get_all_categorie_id(self): # Devuelve los id de las categorias en la tabla categoria
        query = 'SELECT id FROM categoria'
        result = self.db_query(query)
        unique_id = set()
        for r, in result:
            unique_id.add(r)
        return unique_id     


    # METODOS DE ESCRITURA ---------------------------------------------------------------------------------------------
    def add_product(self, name, price, categorie): # Añadimos un producto a la base de datos
        categorie_id, = self.get_categorie_ID(categorie)
        query = 'INSERT INTO producto VALUES (NULL, ?, ?, ?)'
        self.db_query(query, name, price, float(categorie_id))

    def add_categorie(self, categorie): # Añade una nueva categoria a la base de datos
        if not self.item_in_table('categoria', 'nombre', categorie):
            query = 'INSERT INTO categoria VALUES (NULL, ?)'
            self.db_query(query, categorie)
            return True
        return False

    def update_product(self, new_name, new_price, new_categorie, old_name, old_price, old_categorie): # Actualiza un producto, necesitamos el ID de la categoria antigua y nueva
        if new_name and new_price and old_name and old_price:
            old_id, = self.get_categorie_ID(old_categorie) # La coma delante de la variable 'desempaqueta'(unpacks) el resultado, en este caso una tupla de un elemento 
            new_id,= self.get_categorie_ID(new_categorie)
            query = 'UPDATE producto SET nombre = ?, precio = ?, categoriaID = ? WHERE nombre = ? AND precio = ? AND categoriaID = ?'
            self.db_query(query, new_name, new_price, new_id, old_name, old_price, old_id)
            return True
        return False


    # METODOS DE BORRADO ---------------------------------------------------------------------------------------------
    def del_product(self, product): # Elimina un producto
        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_query(query, product)

    def del_categorie(self, categorie): # Elimina un categoria
        query = 'DELETE FROM categoria WHERE nombre = ?'
        self.db_query(query, categorie)

    def del_non_using_categories(self):
        all_ids = self.get_all_categorie_id() # Id's de la tabla categoria
        using_ids = self.get_using_categorie_id() # Id's unicos de la tabla producto
        ids_to_delete = [id for id in all_ids if id not in using_ids] # Id's de la tabla categoria que no se usan en la tabla producto
        for id in ids_to_delete: # Para cada id seleccionado, eliminamos su fila en la tabla
            query = 'DELETE FROM categoria WHERE id = ?'
            self.db_query(query, id)


    # METODOS BOOLEANOS ---------------------------------------------------------------------------------------------
    def item_in_table(self, table, col, item): # Comprueba si un elemento existe en la columna de una tabla
        query = f'SELECT {col} FROM {table}'
        result = self.db_query(query)
        for r, in result:
            if item == r:
                return True
        return False