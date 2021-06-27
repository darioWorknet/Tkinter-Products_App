from tkinter import *
from tkinter import ttk


def new_label(frame, text, fg=None, **kwargs):
    label = Label(frame, text=text, fg=fg)
    label.grid(**kwargs) # Recibe la informacion relativa al layout como **kwargs
    return label

def new_entry(frame, default_txt=None, **kwargs):
    textvariable=StringVar(frame, value=default_txt)
    entry = Entry(frame, textvariable=textvariable)
    entry.grid(**kwargs) # Recibe la informacion relativa al layout como **kwargs
    return entry

def new_button(frame, text, command, **kwargs):
    button = ttk.Button(frame, text=text, command=command)
    button.grid(**kwargs) # Recibe la informacion relativa al layout como **kwargs
    return button

def new_table (*args, **kwargs):
    # Recibe el nombre de las columnas como *args
    # Recibe la informacion relativa al layout como **kwargs
    # Estilo personalizado para la tabla
    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold')) # Se modifica la fuente de las cabeceras
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