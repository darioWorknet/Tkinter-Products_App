from tk_helper import *
from CreateCategorieWindow import CreateCategorieWindow



class EditWindow(Frame):
    def __init__(self, parent, default=None):
        Frame.__init__(self, parent)
        self.window = new_window("Edición de productos")
        self.parent = parent
        self.default = default
        self.create_widgets()

    def create_widgets(self):
        self.create_frame()
        self.update_menu(self.default)

    def create_frame(self):
        # Definimos el frame
        frame = LabelFrame(self.window, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'))
        frame.grid(row=1, column=0, columnspan=2, pady=20)
        # Nombre nuevo
        self.label_name = new_label(frame, "Nombre nuevo: ", row=2, column=0)
        self.entry_name = new_entry(frame, default_txt=self.parent.product_name, row=2, column=1)
        # Precio nuevo
        self.label_price = new_label(frame, "Precio nuevo: ", row=3, column=0)
        self.entry_price = new_entry(frame, default_txt=self.parent.product_price, row=3, column=1)
        # Categoria nueva
        self.label_categorie = new_label(frame, "Categoría nueva: ", row=4, column=0)
        # self.entry_categorie = new_entry(frame, default_txt=self.parent.product_categorie, row=4, column=1)
        categories = self.parent.db.get_categories() # Query to db
        self.categorie_selection = StringVar(frame)
        self.menu_categ = new_option_menu(frame, self.categorie_selection, *categories, row=4, column=1, sticky=W+E)
        self.crete_cat = new_button(frame, '+', self.add_categorie, row=4, column=2, width=3)
        # Boton guardar cambios
        self.update_button = new_button(frame, 'Actualizar producto', self.update_product, row=5, columnspan=2, sticky=W+E)
        # Mensaje
        self.message = new_label(frame, text='', fg='red', row=6, column=0, columnspan=2, sticky=W+E)

    def update_product(self):
        # Obtenemos la informacion del producto
        old_name = self.parent.product_name
        new_name = self.entry_name.get()
        old_price = self.parent.product_price
        new_price = self.entry_price.get()
        old_categorie = self.parent.product_categorie
        new_categorie = self.categorie_selection.get()
        # print("Actualizando producto: ", end='')
        print(f'{old_name=}, {new_name=}, {old_price=}, {new_price=}, {old_categorie=}, {new_categorie=}')
        # Tratamos de actulizar el producto, evaluamos el resultado con un booleano
        updated = self.parent.db.update_product(new_name, new_price, new_categorie, old_name, old_price, old_categorie)
        # Dependiendo de si hemos conseguido actulizar el producto mostramos un aviso u otro
        if updated: # Aviso en la ventana padre
            self.window.destroy() # Cerramos la ventana actual
            self.parent.update_all()
            self.parent.message['text'] = f"Producto {old_name!r} actulizado con éxito\nNuevo nombre: {new_name!r}"
        else: # Aviso en la ventana actual
            self.message['text'] = "Todos los campos son obligatorios"


    def update_menu(self, default=None): # menu, categories, variable, default=None
        update_menu(self.menu_categ, self.parent.db.get_categories(), self.categorie_selection, default)

    def add_categorie(self):
        self.new_categorie_window = CreateCategorieWindow(self)