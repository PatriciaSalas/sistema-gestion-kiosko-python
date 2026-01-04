import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from crud import cliente, producto, carrito
from crud.cliente import autenticar_cliente   
from validaciones import formatear_rut
from api import obtener_datos_api


class InterfazKiosko:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Kiosko Objeto Feliz")
        self.ventana.geometry("1000x600")

        # crear contenedor principal
        self.contenedor_principal = tk.Frame(ventana)
        self.contenedor_principal.pack(fill=tk.BOTH, expand=True)

        # panel izquierdo menu
        self.panel_menu = tk.Frame(self.contenedor_principal, bg="#2c3e50", width=200)
        self.panel_menu.pack(side=tk.LEFT, fill=tk.Y)
        self.panel_menu.pack_propagate(False)

        # panel derecho contenido
        self.panel_contenido = tk.Frame(self.contenedor_principal, bg="#ecf0f1")
        self.panel_contenido.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # crear menu
        self.crear_menu()

        # mostrar vista inicial
        self.mostrar_login()

    def crear_menu(self):
        # crea botones del menu lateral
        titulo = tk.Label(
            self.panel_menu,
            text="MENU",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 16, "bold"),
            pady=20,
        )
        titulo.pack()

        botones = [
            ("Clientes", self.mostrar_clientes),
            ("Productos", self.mostrar_productos),
            ("Carrito", self.mostrar_carrito),
            ("API Externa", self.mostrar_api),
        ]

        for texto, comando in botones:
            btn = tk.Button(
                self.panel_menu,
                text=texto,
                bg="#34495e",
                fg="white",
                font=("Arial", 12),
                relief=tk.FLAT,
                pady=10,
                command=comando,
                cursor="hand2",
            )
            btn.pack(fill=tk.X, padx=10, pady=5)

    def limpiar_panel(self):
        # limpia el panel de contenido
        for widget in self.panel_contenido.winfo_children():
            widget.destroy()

    def mostrar_clientes(self):
        # vista de gestion de clientes
        self.limpiar_panel()

        titulo = tk.Label(
            self.panel_contenido,
            text="Gestion de Clientes",
            bg="#ecf0f1",
            font=("Arial", 18, "bold"),
        )
        titulo.pack(pady=10)

        # frame para formulario
        frame_form = tk.LabelFrame(
            self.panel_contenido,
            text="Datos del Cliente",
            bg="#ecf0f1",
            font=("Arial", 12),
        )
        frame_form.pack(padx=20, pady=10, fill=tk.X)

        # campos del formulario
        tk.Label(frame_form, text="RUT:", bg="#ecf0f1").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        entry_rut = tk.Entry(frame_form, width=30)
        entry_rut.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nombre:", bg="#ecf0f1").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )
        entry_nombre = tk.Entry(frame_form, width=30)
        entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Apellido:", bg="#ecf0f1").grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W
        )
        entry_apellido = tk.Entry(frame_form, width=30)
        entry_apellido.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Correo:", bg="#ecf0f1").grid(
            row=3, column=0, padx=5, pady=5, sticky=tk.W
        )
        entry_correo = tk.Entry(frame_form, width=30)
        entry_correo.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Telefono:", bg="#ecf0f1").grid(
            row=4, column=0, padx=5, pady=5, sticky=tk.W
        )
        entry_telefono = tk.Entry(frame_form, width=30)
        entry_telefono.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Contrasena:", bg="#ecf0f1").grid(
            row=5, column=0, padx=5, pady=5, sticky=tk.W
        )
        entry_pass = tk.Entry(frame_form, width=30, show="*")
        entry_pass.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nivel:", bg="#ecf0f1").grid(
            row=6, column=0, padx=5, pady=5, sticky=tk.W
        )
        combo_nivel = ttk.Combobox(
            frame_form, values=["General", "Estudiante"], width=28, state="readonly"
        )
        combo_nivel.set("General")
        combo_nivel.grid(row=6, column=1, padx=5, pady=5)

        # frame para listado
        frame_lista = tk.LabelFrame(
            self.panel_contenido,
            text="Clientes Registrados",
            bg="#ecf0f1",
            font=("Arial", 12),
        )
        frame_lista.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(
            frame_lista,
            columns=("RUT", "Nombre", "Apellido", "Correo", "Telefono", "Nivel"),
            show="headings",
            height=8,
        )
        tree.heading("RUT", text="RUT")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Apellido", text="Apellido")
        tree.heading("Correo", text="Correo")
        tree.heading("Telefono", text="Telefono")
        tree.heading("Nivel", text="Nivel")
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # funciones internas
        def actualizar_lista():
            tree.delete(*tree.get_children())
            clientes = cliente.obtener_clientes()
            for cli in clientes:
                tree.insert("", tk.END, values=cli)

        def crear():
            # CORRECCIÓN CLAVE: Usar .strip() para asegurar que no haya espacios
            rut_limpio = entry_rut.get().strip() 
            
            # Pasar el RUT limpio a la función de formateo
            rut_a_enviar = formatear_rut(rut_limpio)
            
            exito, mensaje = cliente.crear_cliente(
                rut_a_enviar, # <-- Usar la variable limpia y formateada
                entry_nombre.get(),
                entry_apellido.get(),
                entry_correo.get(),
                entry_telefono.get(),
                entry_pass.get(),
                combo_nivel.get(),
            )
            messagebox.showinfo("Resultado", mensaje)
            if exito:
                actualizar_lista()

        def seleccionar(event):
            sel = tree.selection()
            if sel:
                vals = tree.item(sel[0])["values"]
                entry_rut.delete(0, tk.END)
                entry_rut.insert(0, vals[0])
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, vals[1])
                entry_apellido.delete(0, tk.END)
                entry_apellido.insert(0, vals[2])
                entry_correo.delete(0, tk.END)
                entry_correo.insert(0, vals[3])
                entry_telefono.delete(0, tk.END)
                entry_telefono.insert(0, vals[4])
                combo_nivel.set(vals[5])

        tree.bind("<Double-1>", seleccionar)

        # botones
        frame_btn = tk.Frame(frame_form, bg="#ecf0f1")
        frame_btn.grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(
            frame_btn, text="Crear", bg="#27ae60", fg="white", command=crear, width=10
        ).pack(side=tk.LEFT, padx=5)

        actualizar_lista()

    def mostrar_productos(self):
        # vista de gestion de productos
        self.limpiar_panel()

        titulo = tk.Label(
            self.panel_contenido,
            text="Gestion de Productos",
            bg="#ecf0f1",
            font=("Arial", 18, "bold"),
        )
        titulo.pack(pady=10)

        frame_form = tk.LabelFrame(
            self.panel_contenido,
            text="Datos del Producto",
            bg="#ecf0f1",
            font=("Arial", 12),
        )
        frame_form.pack(padx=20, pady=10, fill=tk.X)

        tk.Label(frame_form, text="Nombre:", bg="#ecf0f1").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        entry_nombre = tk.Entry(frame_form, width=30)
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Precio Neto:", bg="#ecf0f1").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )
        entry_precio = tk.Entry(frame_form, width=30)
        entry_precio.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Stock:", bg="#ecf0f1").grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W
        )
        entry_stock = tk.Entry(frame_form, width=30)
        entry_stock.grid(row=2, column=1, padx=5, pady=5)

        frame_lista = tk.LabelFrame(
            self.panel_contenido,
            text="Productos Disponibles",
            bg="#ecf0f1",
            font=("Arial", 12),
        )
        frame_lista.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(
            frame_lista,
            columns=("ID", "Nombre", "Precio Neto", "Precio IVA", "Stock"),
            show="headings",
            height=8,
        )
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Precio Neto", text="Precio Neto")
        tree.heading("Precio IVA", text="Precio + IVA")
        tree.heading("Stock", text="Stock")
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        def actualizar_lista():
            tree.delete(*tree.get_children())
            productos = producto.obtener_productos()
            for prod in productos:
                precio_iva = prod[2] * 1.19
                tree.insert(
                    "",
                    tk.END,
                    values=(
                        prod[0],
                        prod[1],
                        f"${prod[2]:.2f}",
                        f"${precio_iva:.2f}",
                        prod[3],
                    ),
                )

        def crear():
            exito, mensaje = producto.crear_producto(
                entry_nombre.get(), float(entry_precio.get()), int(entry_stock.get())
            )
            messagebox.showinfo("Resultado", mensaje)
            if exito:
                actualizar_lista()

        frame_btn = tk.Frame(frame_form, bg="#ecf0f1")
        frame_btn.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(
            frame_btn, text="Crear", bg="#27ae60", fg="white", command=crear, width=10
        ).pack(side=tk.LEFT, padx=5)

        actualizar_lista()

    def mostrar_carrito(self):
        # vista de gestion de carrito
        self.limpiar_panel()

        titulo = tk.Label(
            self.panel_contenido,
            text="Carrito de Compras",
            bg="#ecf0f1",
            font=("Arial", 18, "bold"),
        )
        titulo.pack(pady=10)

        frame_superior = tk.Frame(self.panel_contenido, bg="#ecf0f1")
        frame_superior.pack(padx=20, pady=10, fill=tk.X)

        # seleccion cliente
        frame_cli = tk.LabelFrame(
            frame_superior, text="Cliente", bg="#ecf0f1", font=("Arial", 12)
        )
        frame_cli.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        clientes_lista = cliente.obtener_clientes()
        clientes_dict = {f"{c[0]} - {c[1]} {c[2]}": c[0] for c in clientes_lista}

        combo_clientes = ttk.Combobox(
            frame_cli, values=list(clientes_dict.keys()), width=35, state="readonly"
        )
        combo_clientes.pack(padx=10, pady=10)

        id_carrito_actual = tk.StringVar(value="")

        def crear_carrito():
            if combo_clientes.get():
                rut = clientes_dict[combo_clientes.get()]
                exito, resultado = carrito.crear_carrito(rut)
                if exito:
                    id_carrito_actual.set(str(resultado))
                    messagebox.showinfo("Exito", f"Carrito creado: {resultado}")

        tk.Button(
            frame_cli,
            text="Crear Carrito",
            bg="#3498db",
            fg="white",
            command=crear_carrito,
        ).pack(pady=5)

        # agregar productos
        frame_prod = tk.LabelFrame(
            frame_superior, text="Agregar Producto", bg="#ecf0f1", font=("Arial", 12)
        )
        frame_prod.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        productos_lista = producto.obtener_productos()
        productos_dict = {f"{p[0]} - {p[1]}": p[0] for p in productos_lista}

        combo_productos = ttk.Combobox(
            frame_prod, values=list(productos_dict.keys()), width=25, state="readonly"
        )
        combo_productos.pack(padx=10, pady=5)

        tk.Label(frame_prod, text="Cantidad:", bg="#ecf0f1").pack()
        entry_cantidad = tk.Entry(frame_prod, width=10)
        entry_cantidad.pack(pady=5)

        # detalles
        frame_det = tk.LabelFrame(
            self.panel_contenido, text="Detalles", bg="#ecf0f1", font=("Arial", 12)
        )
        frame_det.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(
            frame_det,
            columns=("Producto", "P.Neto", "P.IVA", "Cant", "Subtotal"),
            show="headings",
            height=6,
        )
        tree.heading("Producto", text="Producto")
        tree.heading("P.Neto", text="P.Neto")
        tree.heading("P.IVA", text="P.IVA")
        tree.heading("Cant", text="Cant")
        tree.heading("Subtotal", text="Subtotal")
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # totales
        frame_tot = tk.LabelFrame(
            self.panel_contenido, text="Totales", bg="#ecf0f1", font=("Arial", 12)
        )
        frame_tot.pack(padx=20, pady=10, fill=tk.X)

        lbl_sub = tk.Label(
            frame_tot, text="Subtotal: $0.00", bg="#ecf0f1", font=("Arial", 12)
        )
        lbl_sub.pack(pady=5)
        lbl_desc = tk.Label(
            frame_tot, text="Descuento: $0.00", bg="#ecf0f1", font=("Arial", 12)
        )
        lbl_desc.pack(pady=5)
        lbl_tot = tk.Label(
            frame_tot, text="Total: $0.00", bg="#ecf0f1", font=("Arial", 12, "bold")
        )
        lbl_tot.pack(pady=5)

        def actualizar_carrito():
            if not id_carrito_actual.get():
                return

            tree.delete(*tree.get_children())
            rut = clientes_dict[combo_clientes.get()]
            totales = carrito.calcular_totales(int(id_carrito_actual.get()), rut)

            if totales:
                for det in totales["detalles"]:
                    id_p, nom, pn, st, cant = det
                    piva = pn * 1.19
                    subt = piva * cant
                    tree.insert(
                        "",
                        tk.END,
                        values=(
                            nom,
                            f"${pn:.2f}",
                            f"${piva:.2f}",
                            cant,
                            f"${subt:.2f}",
                        ),
                    )

                lbl_sub.config(text=f"Subtotal: ${totales['subtotal']:.2f}")
                lbl_desc.config(text=f"Descuento: ${totales['descuento']:.2f}")
                lbl_tot.config(text=f"Total: ${totales['total']:.2f}")

        def agregar():
            if not id_carrito_actual.get():
                messagebox.showwarning("Advertencia", "Crea un carrito primero")
                return
            if combo_productos.get() and entry_cantidad.get():
                id_p = productos_dict[combo_productos.get()]
                cant = int(entry_cantidad.get())
                exito, msg = carrito.agregar_detalle(
                    int(id_carrito_actual.get()), id_p, cant
                )
                messagebox.showinfo("Resultado", msg)
                if exito:
                    actualizar_carrito()

        tk.Button(
            frame_prod, text="Agregar", bg="#27ae60", fg="white", command=agregar
        ).pack(pady=5)

        def mostrar_voucher():
            if not id_carrito_actual.get():
                messagebox.showwarning("Advertencia", "No hay carrito")
                return
            rut = clientes_dict[combo_clientes.get()]
            voucher_txt = carrito.generar_voucher(int(id_carrito_actual.get()), rut)

            ventana_v = tk.Toplevel(self.ventana)
            ventana_v.title("Voucher")
            ventana_v.geometry("500x600")

            txt = scrolledtext.ScrolledText(
                ventana_v, width=60, height=30, font=("Courier", 10)
            )
            txt.pack(padx=10, pady=10)
            txt.insert(tk.END, voucher_txt)
            txt.config(state=tk.DISABLED)

        tk.Button(
            frame_tot,
            text="Generar Voucher",
            bg="#9b59b6",
            fg="white",
            font=("Arial", 12),
            command=mostrar_voucher,
        ).pack(pady=10)

    def mostrar_api(self):
        # vista de api externa
        self.limpiar_panel()

        titulo = tk.Label(
            self.panel_contenido,
            text="API Externa",
            bg="#ecf0f1",
            font=("Arial", 18, "bold"),
        )
        titulo.pack(pady=10)

        frame_btn = tk.Frame(self.panel_contenido, bg="#ecf0f1")
        frame_btn.pack(pady=20)

        frame_res = tk.LabelFrame(
            self.panel_contenido, text="Resultados", bg="#ecf0f1", font=("Arial", 12)
        )
        frame_res.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        txt_res = scrolledtext.ScrolledText(
            frame_res, width=70, height=15, font=("Arial", 11)
        )
        txt_res.pack(padx=10, pady=10)

        def obtener_clima():
            txt_res.delete(1.0, tk.END)
            txt_res.insert(tk.END, "Consultando clima...\n\n")
            datos = obtener_datos_api("clima")
            if "error" in datos:
                txt_res.insert(tk.END, f"Error: {datos['error']}")
            else:
                txt_res.insert(tk.END, "CLIMA ACTUAL\n" + "=" * 40 + "\n")
                txt_res.insert(tk.END, f"Ciudad: {datos['ciudad']}\n")
                txt_res.insert(tk.END, f"Temperatura: {datos['temperatura']}\n")
                txt_res.insert(tk.END, f"Descripcion: {datos['descripcion']}\n")
                txt_res.insert(tk.END, f"Humedad: {datos['humedad']}\n")

        def obtener_dolar():
            txt_res.delete(1.0, tk.END)
            txt_res.insert(tk.END, "Consultando conversion...\n\n")
            datos = obtener_datos_api("dolar")
            if "error" in datos:
                txt_res.insert(tk.END, f"Error: {datos['error']}")
            else:
                txt_res.insert(tk.END, "CONVERSION MONEDA\n" + "=" * 40 + "\n")
                txt_res.insert(tk.END, f"Moneda: {datos['moneda']}\n")
                txt_res.insert(tk.END, f"Valor: {datos['valor']}\n")
                txt_res.insert(tk.END, f"Fecha: {datos['fecha']}\n")

        tk.Button(
            frame_btn,
            text="Obtener Clima",
            bg="#3498db",
            fg="white",
            font=("Arial", 12),
            width=20,
            command=obtener_clima,
        ).pack(side=tk.LEFT, padx=10)
        tk.Button(
            frame_btn,
            text="Valor Dolar",
            bg="#e67e22",
            fg="white",
            font=("Arial", 12),
            width=20,
            command=obtener_dolar,
        ).pack(side=tk.LEFT, padx=10)

    def mostrar_login(self):
        self.limpiar_panel()

        frame = tk.Frame(self.panel_contenido, bg="#ecf0f1")
        frame.pack(expand=True)

        tk.Label(frame, text="Login", font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=10)

        tk.Label(frame, text="RUT:", bg="#ecf0f1").pack()
        entry_rut = tk.Entry(frame, width=30)
        entry_rut.pack(pady=5)

        tk.Label(frame, text="Contraseña:", bg="#ecf0f1").pack()
        entry_pass = tk.Entry(frame, width=30, show="*")
        entry_pass.pack(pady=5)

        def login():
            rut = formatear_rut(entry_rut.get().strip())
            contrasena = entry_pass.get()

            ok, resultado = autenticar_cliente(rut, contrasena)

            if ok:
                self.cliente_actual = resultado
                messagebox.showinfo("Éxito", f"Bienvenido {resultado.nombre}")
                self.mostrar_clientes()  # entra al sistema
            else:
                messagebox.showerror("Error", resultado)

        tk.Button(
            frame,
            text="Ingresar",
            bg="#27ae60",
            fg="white",
            font=("Arial", 12),
            command=login,
            width=15,
        ).pack(pady=10)