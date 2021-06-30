from tk_helper import *


class CreateCategorieWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.window = new_window("Añadir nueva categoria")
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.create_frame()

    def create_frame(self):
        # Definimos el frame
        frame = LabelFrame(self.window, text="Introduce nueva categoría", font=('Calibri', 16, 'bold'))
        frame.grid(row=1, column=0, columnspan=2, pady=20)
        # Categoria nueva
        self.label_name = new_label(frame, "Nueva categoría: ", row=2, column=0)
        self.entry_name = new_entry(frame, row=2, column=1)
        self.entry_name.focus()
        # Boton guardar cambios
        self.update_button = new_button(frame, 'Añadir', self.commit_changes, row=3, columnspan=2, sticky=W+E)
        # Boton eliminar categorias en desuso
        self.update_button = new_button(frame, 'Eliminar categorias en desuso', self.parent.del_non_using_categories, row=4, columnspan=2, sticky=W+E)
        # Mensaje
        self.message = new_label(frame, text='', fg='red', row=5, column=0, columnspan=2, sticky=W+E)

    def commit_changes(self):
        # Cogemos la categoria introducida por el usuario
        new_categorie = self.entry_name.get()
        # Comprobamos que haya introducido algun dato
        if new_categorie:
            # Introducimos la categoria en la base de datos
            # Puede que se haya llamado a este metodo desde una instancia de ProductWindow o EditWindow
            # Dependiendo del caso, la relacion de parentesco entre objetos cambia
            try:
                query_result = self.parent.db.add_categorie(new_categorie)
            except Exception:
                query_result = self.parent.parent.db.add_categorie(new_categorie)
            # Si el resultado de la query ha sido positivo
            if query_result:
                self.window.destroy() # Cerramos la ventana actual
                self.parent.update_menu(new_categorie) # Actulizamos el desplegable en la ventana padre
                self.parent.message["text"] = f"Categoría {new_categorie!r} añadida con éxito a la base de datos"
            else:
                self.message["text"] = "El elemento ya existe en la base de datos"
        # En caso de que no haya introducido ninguna categoria, mostramos el siguiente aviso
        else:
            self.message["text"] = "Debes introducir una categoria"