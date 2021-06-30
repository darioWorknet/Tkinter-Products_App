import tkinter as tk
from ProductWindow import ProductWindow


if __name__ == "__main__":
    root = tk.Tk()
    app = ProductWindow(root)
    app.mainloop()