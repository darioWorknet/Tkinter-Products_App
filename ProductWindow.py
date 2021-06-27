from EditWindow import EditWindow
from tkinter import *
from tk_helper import *
from db_helper import DB

class ProductWindow(Frame):
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
        frame = LabelFrame(self.master, text="Registrar un nuevo Producto", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=2, pady=20)
        # Nombre del producto
        self.label_name = new_label(frame, 'Nombre: ', row=1, column=0)
        self.entry_name = new_entry(frame, row=1, column=1)
        # Precio
        self.label_price = new_label(frame, 'Precio: ', row=2, column=0)
        self.entry_price = new_entry(frame, row=2, column=1)
        # Boton
        self.button_add = new_button(frame, 'Guardar producto', self.add_product, row=3, columnspan=2, sticky=W+E)
        # Mensaje
        self.message = new_label(frame=None, text='', fg='red', row=3, column=0, columnspan=2, sticky=W+E)
    
    def create_table(self):
        self.table = new_table('Nombre', 'Precio', row=4, column=0, columnspan=2)
        self.fill_table()

    def create_action_buttons(self):
        self.delete_button = new_button(None, 'ELIMINAR', self.del_product, row=5, columnspan=1, column=0, sticky=W+E)
        self.edit_button = new_button(None, 'EDITAR', self.edit_product, row=5, columnspan=1, column=1, sticky=W+E)

    def add_product(self):
        # Atributos del producto
        product_name = self.entry_name.get()
        product_price = self.entry_price.get()
        if product_name and product_price:
            print("Producto anadido")
            self.message['text'] = f'Producto {product_name!r} añadido con éxito'
            self.db.add_product(product_name, product_price)
            self.fill_table()
        elif not product_name and product_price:
            print('El nombre es obligatorio')
            self.message['text'] = 'El nombre es obligatorio'
        elif product_name and not product_price:
            print('El precio es obligatorio')
            self.message['text'] = 'El precio es obligatorio'
        else:
            print('El nombre y el precio son obligatorios')
            self.message['text'] = 'El nombre y el precio son obligatorios'

    def fill_table(self):
        # Limpiar la tabla
        table_rows = self.table.get_children()
        for row in table_rows:
            self.table.delete(row)
        # Ejecutar la consulta
        products = self.db.get_products()
        # Rellenar la tabla
        for product in products:
            print(product)
            self.table.insert('', 0, text=product[1], values=product[2])

    def del_product(self):
        product_name = self.table.item(self.table.selection())['text']
        if product_name:
            # print(f"Borrando producto: {product_name}")
            self.db.del_product(product_name)
            self.fill_table()
            self.message['text'] = f"Producto {product_name!r} eliminado con éxito"
        else:
            # print("Por favor seleccione un producto")
            self.message['text'] = "Por favor seleccione un producto"

    def edit_product(self):
        self.product_name = self.table.item(self.table.selection())['text']
        values = self.table.item(self.table.selection())['values']
        if self.product_name and values:
            self.product_price = values[0]
            # print(f"Fila seleccionada: {self.product_name = } {self.product_price = }")
            self.edit_window = EditWindow(self)
        else:
            # print("Por favor seleccione un producto")
            self.message['text'] = "Por favor seleccione un producto"
            return

    def say_hello(self):
        print("Hello from parent class")