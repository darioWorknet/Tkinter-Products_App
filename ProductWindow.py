from CreateCategorieWindow import CreateCategorieWindow
from EditWindow import EditWindow
from tkinter import *
from tk_helper import *
from db_helper import DB


class ProductWindow(Frame):
    # Estilos
    TEXT = ('Calibri', 13)
    BUTTON = ('Calibri', 14, 'bold')
    TITLE =('Calibri', 16, 'bold')

    def __init__(self, master):
        super().__init__(master)
        self.master = master # root
        self.db = DB('database/productos.db') # conexion con la base de datos
        self.create_widgets() # Elementos graficos

    def create_widgets(self):
        self.edit_window()
        self.create_frame()
        self.create_table()
        self.create_action_buttons()

    def edit_window(self): # Redimensionable por defecto
        self.master.title("App gestor de productos")
        self.master.resizable(1,1)
        self.master.wm_iconbitmap('recursos/icon.ico')

    def create_frame(self):
        # Creacion del frame (padre)
        frame = LabelFrame(self.master, text="Registrar un nuevo Producto", font=self.TITLE)
        frame.grid(row=0, column=0, columnspan=2, pady=20)
        # Nombre del producto
        self.label_name = new_label(frame, 'Nombre: ',  font=self.TEXT, row=1, column=0)
        self.entry_name = new_entry(frame, font=self.TEXT, row=1, column=1)
        # Precio
        self.label_price = new_label(frame, 'Precio: ', font=self.TEXT, row=2, column=0)
        self.entry_price = new_entry(frame, font=self.TEXT, row=2, column=1)
        # Categoria
        self.label_categ = new_label(frame, 'Categoria: ', font=self.TEXT, row=3, column=0)
        categories = self.db.get_categories() # Query to db
        self.categorie_selection = StringVar(frame)
        self.menu_categ = new_option_menu(frame, self.categorie_selection, *categories,  font=self.TEXT, row=3, column=1, sticky=W+E)
        self.crete_cat = new_button(frame, '+', self.add_categorie, font=self.BUTTON, row=3, column=2, width=3)
        # Boton
        self.button_add = new_button(frame, 'Guardar producto', self.add_product, font=self.BUTTON, row=4, columnspan=2, sticky=W+E)
        # Mensaje
        self.message = new_label(frame=None, text='', fg='red', row=5, column=0, columnspan=2, sticky=W+E)
    
    def create_table(self):
        # Metodo  de tk helper, nos permite crear una tabla pasandole el nombre de las columnas
        self.table = new_table('Nombre', 'Precio', 'Categoría', row=6, column=0, columnspan=2)
        self.fill_table()

    def create_action_buttons(self):
        # Botones que llaman a los metodos para eliminar y editar los productos
        self.delete_button = new_button(None, 'ELIMINAR', self.del_product,  font=self.BUTTON, row=7, columnspan=1, column=0, sticky=W+E) # del.product
        self.edit_button = new_button(None, 'EDITAR', self.edit_product, font=self.BUTTON, row=7, columnspan=1, column=1, sticky=W+E) # edit.product

    def add_product(self):
        # Atributos del producto
        product_name = self.entry_name.get()
        product_price = self.entry_price.get()
        product_categorie = self.categorie_selection.get()
        if not product_price.replace('.','',1).isnumeric(): # Comprobamos que el valor introducido sea un numero entero o decimal
            self.message['text'] = f'El precio debe ser un valor numérico'
        elif product_name and product_price and product_categorie: # Si se introducen los 3 campos se guarda en la base de datos
            self.db.add_product(product_name, product_price, product_categorie) # Metodo que introduce el producto en la base de datos
            self.update_all()
            self.message['text'] = f'Producto {product_name!r} añadido con éxito'
        elif not product_name and product_price and product_categorie: # Casos en los que falta algun campo
            self.message['text'] = 'El nombre es obligatorio'
        elif product_name and not product_price and product_categorie:
            self.message['text'] = 'El precio es obligatorio'
        elif product_name and product_price and not product_categorie:
            self.message['text'] = 'La categoría es obligatoria'
        else: 
            self.message['text'] = 'Todos los campos son obligatorios'

    def fill_table(self):
        # Limpiar la tabla
        table_rows = self.table.get_children()
        for row in table_rows:
            self.table.delete(row)
        # Ejecutar la consulta
        products = self.db.get_products()
        # Rellenar la tabla
        for product in products:
            self.table.insert('', 0, text=product[0], values=(product[1], product[2]))

    def del_product(self):
        product_name = self.table.item(self.table.selection())['text'] # Obtenemos el nombre del producto seleccionado
        if product_name:                       # Comprobamos que se haya seleccionado alguna fila de la tabla
            self.db.del_product(product_name)  # LLamamos al metodo que borra una fila de la base de datos dado un producto
            self.fill_table()                  # Actualizamos los valores de la tabla
            self.message['text'] = f"Producto {product_name!r} eliminado con éxito"
        else:
            self.message['text'] = "Por favor seleccione un producto"

    def edit_product(self):
        self.product_name = self.table.item(self.table.selection())['text'] # Obtenemos la primera columna (nombre)
        values = self.table.item(self.table.selection())['values'] # Obtenemos el resto de columnas
        if self.product_name and values:
            self.product_price = values[0]     # Precio
            self.product_categorie = values[1] # Categoria
            # Creamos una ventana auxiliar para insertar los nuevos campos del producto
            # Le pasamos la instancia de esta clase (para acceder a ciertos atributos) y la categoria por defecto
            self.edit_window = EditWindow(self, self.product_categorie)
        else:
            self.message['text'] = "Por favor seleccione un producto"

    def add_categorie(self):
        # Creamos una ventana auxiliar para crear una nueva categoria
        # Le pasamos la instancia de esta clase para acceder a ciertos atriburos y metodos
        self.new_categorie_window = CreateCategorieWindow(self)

    def update_menu(self, default=None):
        # Metodo de tk_helper, creado para reutilizar el codigo
        update_menu(self.menu_categ, self.categorie_selection, self.db.get_categories(), default)

    def update_all(self):
        self.fill_table()
        self.update_menu()
        self.entry_name.delete(0, 'end')
        self.entry_price.delete(0, 'end')

    def del_non_using_categories(self):
        # Metodo que elimina las categorias que no estan siendo utilizadas en la tabla producto
        self.db.del_non_using_categories()
        # Actualizamos los campos del menu desplegable
        self.update_menu()