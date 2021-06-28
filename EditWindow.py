from tk_helper import *


class EditWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.window = new_window("Edición de productos")
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.create_frame()

    def create_frame(self):
        # Definimos el frame
        frame = LabelFrame(self.window, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'))
        frame.grid(row=1, column=0, columnspan=2, pady=20)
        # Nombre nuevo
        self.label_name = new_label(frame, "Nombre nuevo: ", row=2, column=0)
        self.entry_name = new_entry(frame, default_txt=self.parent.product_name, row=2, column=1)
        # Precio nuevo
        self.label_price = new_label(frame, "Nombre nuevo: ", row=3, column=0)
        self.entry_price = new_entry(frame, default_txt=self.parent.product_price, row=3, column=1)
        # Boton guardar cambios
        self.update_button = new_button(frame, 'Actualizar producto', self.update_product, row=4, columnspan=2, sticky=W+E)
        # Mensaje
        self.message = new_label(frame, text='', fg='red', row=5, column=0, columnspan=2, sticky=W+E)

    def update_product(self):
        # Obtenemos la informacion del producto
        old_name = self.parent.product_name
        new_name = self.entry_name.get()
        old_price = self.parent.product_price
        new_price = self.entry_price.get()
        # print("Actualizando producto: ", end='')
        # print(f'{old_name=}, {new_name=}, {old_price=}, {new_price=}')
        self.parent.say_hello()
        # Tratamos de actulizar el producto, evaluamos el resultado con un booleano
        updated = self.parent.db.update_product(new_name, new_price, old_name, old_price)
        # Dependiendo de si hemos conseguido actulizar el producto mostramos un aviso u otro
        if updated: # Aviso en la ventana padre
            self.window.destroy() # Cerramos la ventana actual
            self.parent.update_all()
            self.parent.message['text'] = f"Producto {old_name!r} actulizado con éxito\nNuevo nombre: {new_name!r}"
        else: # Aviso en la ventana actual
            self.message['text'] = "Todos los campos son obligatorios"