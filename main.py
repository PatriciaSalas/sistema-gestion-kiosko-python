import tkinter as tk
from interfaz import InterfazKiosko

# punto de entrada del sistema kiosko objeto feliz
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = InterfazKiosko(ventana_principal)
    ventana_principal.mainloop()
