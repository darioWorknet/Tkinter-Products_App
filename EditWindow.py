from tk_helper import *
from CreateCategorieWindow import CreateCategorieWindow



class EditWindow(Frame):
    # Estilos
    TEXT = ('Calibri', 13)
    BUTTON = ('Calibri', 14, 'bold')
    TITLE =('Calibri', 16, 'bold')

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
        frame = LabelFrame(self.window, text="Editar el siguiente Producto", font=self.TITLE)
        frame.grid(row=1, column=0, columnspan=2, pady=20)
        # Nombre nuevo
        self.label_name = new_label(frame, "Nombre nuevo: ", font=self.TEXT, row=2, column=0)
        self.entry_name = new_entry(frame, default_txt=self.parent.product_name, font=self.TEXT, row=2, column=1)
        # Precio nuevo
        self.label_price = new_label(frame, "Precio nuevo: ", font=self.TEXT, row=3, column=0)
        self.entry_price = new_entry(frame, default_txt=self.parent.product_price, font=self.TEXT, row=3, column=1)
        # Categoria nueva
        self.label_categorie = new_label(frame, "Categoría nueva: ", font=self.TEXT, row=4, column=0)
        categories = self.parent.db.get_categories() # Query to db
        self.categorie_selection = StringVar(frame)
        self.menu_categ = new_option_menu(frame, self.categorie_selection, *categories,  font=self.TEXT, row=4, column=1, sticky=W+E)
        self.crete_cat = new_button(frame, '+', self.add_categorie, font=self.BUTTON, row=4, column=2, width=3)
        # Boton guardar cambios
        self.update_button = new_button(frame, 'Actualizar producto', self.update_product, font=self.BUTTON, row=5, columnspan=2, sticky=W+E)
        # Mensaje
        self.message = new_label(frame, text='', fg='red', font=self.TEXT, row=6, column=0, columnspan=2, sticky=W+E)

    def update_product(self):
        # Obtenemos la informacion del producto, tanto la previa como la nueva
        old_name = self.parent.product_name
        new_name = self.entry_name.get()
        old_price = self.parent.product_price
        new_price = self.entry_price.get()
        old_categorie = self.parent.product_categorie
        new_categorie = self.categorie_selection.get()
        if (old_name == new_name) and (old_price == new_price) and (old_categorie == new_categorie):
            self.message['text'] = "No se han actualizado los campos"
            return
        # Tratamos de actulizar el producto, evaluamos el resultado con un booleano
        updated = self.parent.db.update_product(new_name, new_price, new_categorie, old_name, old_price, old_categorie)
        # Dependiendo de si hemos conseguido actulizar el producto mostramos un aviso u otro
        if updated: # Aviso en la ventana padre
            self.window.destroy() # Cerramos la ventana actual
            self.parent.update_all()
            self.parent.message['text'] = f"Producto {old_name!r} actulizado con éxito\nNuevo nombre: {new_name!r}"
        else: # Aviso en la ventana actual
            self.message['text'] = "Todos los campos son obligatorios"


    def update_menu(self, default=None):
        # Metodo de tk_helper, para reutilizar el codigo
        update_menu(self.menu_categ, self.categorie_selection, self.parent.db.get_categories(), default)
        self.parent.update_menu(default) # Actualizamos a su vez el menu de la ventana padre

    def add_categorie(self):
        # Creamos una ventana auxiliar para introducir una nueva categoria
        # Le pasamos la instancia de esta clase (para acceder a ciertos atributos) y la categoria por defecto
        self.new_categorie_window = CreateCategorieWindow(self)