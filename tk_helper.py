from tkinter import *
from tkinter import ttk


def new_label(frame, text, font=None, fg=None, **kwargs):
    label = Label(frame, text=text, font=font, fg=fg)
    label.grid(**kwargs) # Recibe la informacion relativa al layout como **kwargs
    return label

def new_entry(frame, default_txt=None, font=None, **kwargs):
    textvariable=StringVar(frame, value=default_txt)
    entry = Entry(frame, textvariable=textvariable, font=font, justify='center')
    entry.grid(**kwargs) # Recibe la informacion relativa al layout como **kwargs
    return entry

def new_button(frame, text, command, font=None, width=None, **kwargs):
    style=None
    if font: # Definimos un estilo, si recibe una fuente
        s = ttk.Style()
        s.configure('my.TButton', font=font)
        style = 'my.TButton'
    button = ttk.Button(frame, text=text, command=command, style=style, width=width)
    button.grid(**kwargs) # Recibe la informacion relativa al layout como **kwargs
    return button

def new_option_menu(frame, variable, *categories, font=None, **kwargs):
    variable.set("") # Variable que apunta al elemento seleccionado, la inicializamos en blanco
    if categories:
        variable.set(categories[0]) # Si recibe elementos, mostramos el primero
        categories = [""]
    option_menu = OptionMenu(frame, variable, *categories) # Creamos el widget
    # Definimos el estilo del texto
    if font:
        option_menu.config(font=font)
    option_menu.grid(**kwargs) # Recibe la informacion relativa al layout como kwargs  
    return option_menu

def new_table (*args, **kwargs):
    # Recibe el nombre de las columnas como *args
    # Recibe la informacion relativa al layout como **kwargs
    # Estilo personalizado para la tabla
    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 13)) # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 14, 'bold')) # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Eliminamos los bordes
    # Estructura de la tabla
    cols = tuple([f'#{i}' for i in range(len(args)-1)])
    table = ttk.Treeview(height=20, columns=cols, style="mystyle.Treeview")
    table.grid(**kwargs)
    for i, arg in enumerate(args):
        table.heading(f'#{i}', text=arg, anchor=CENTER) # Encabezado
    return table

def new_window(title):
    window = Toplevel() # Crear una ventana por delante de la principal
    window.title(title) # Titulo de la ventana
    window.resizable(1, 1) # Activar la redimension de la ventana. Para desactivarla: (0,0)
    window.wm_iconbitmap('recursos/icon.ico') # Icono de la ventana
    return window

def update_menu(this_menu, variable, items, default=None):
    this_menu['menu'].delete(0,'end') # Borramos el contenido del boton
    if not items:
        items = ['']
    for item in items:           # Introducimos los nuevos elementos
        this_menu['menu'].add_command(label=item, command=lambda x=item: variable.set(x))
    if default:
        variable.set(default)   # Mostramos el valor por defecto
    elif items:
        variable.set(items[0])  # En caso contrario mostramos el primer elemento de la lista