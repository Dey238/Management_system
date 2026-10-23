"""Ventanas modales para las operaciones del sistema."""

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from Datos.acceso_a_datos import ClienteDAO, ProductoDAO, ProveedorDAO, VentaDAO

from .componentes import TablaTarjeta, crear_combo, indice_combo
from .config import BG, BG_MENU, MARRON, MARRON_OSCURO, RADIO


class FormularioBase(ctk.CTkToplevel):
    def __init__(self, parent, titulo, dimensiones):
        super().__init__(parent)
        self.title(titulo)
        self.geometry(dimensiones)
        self.configure(fg_color=BG)
        self.resizable(False, False)
        self.transient(parent)
        self.after(150, self.grab_set)
        self.focus()

    def crear_label(self, texto, es_titulo=False):
        if es_titulo:
            ctk.CTkLabel(self, text=texto, text_color=MARRON_OSCURO, font=("Arial", 20, "bold")).pack(
                pady=(20, 15)
            )
        else:
            ctk.CTkLabel(self, text=texto, text_color=MARRON, font=("Arial", 13, "bold")).pack(
                anchor="w", padx=40
            )

    def crear_entrada(self):
        entrada = ctk.CTkEntry(
            self,
            height=38,
            corner_radius=RADIO,
            fg_color="white",
            text_color="black",
            border_width=0,
            font=("Arial", 14),
        )
        entrada.pack(fill=tk.X, padx=40, pady=(2, 10))
        return entrada

    def crear_combo(self, opciones):
        combo = crear_combo(self, opciones)
        combo.pack(fill=tk.X, padx=40, pady=(2, 10))
        return combo

    def crear_boton(self, texto, comando):
        ctk.CTkButton(
            self,
            text=texto,
            command=comando,
            height=38,
            corner_radius=RADIO,
            fg_color=MARRON,
            hover_color=MARRON_OSCURO,
            text_color="white",
            font=("Arial", 14, "bold"),
        ).pack(fill=tk.X, padx=40, pady=(15, 20))


class VentanaNuevaVenta(FormularioBase):
    def __init__(self, parent, al_guardar_callback):
        super().__init__(parent, "Procesar Nueva Venta", "720x640")
        self.al_guardar_callback = al_guardar_callback
        self.carrito = []
        self.lista_productos_cache = []
        self.lista_clientes_cache = []
        self._cargar_datos_combo()
        self._crear_interfaz_venta()

    def _cargar_datos_combo(self):
        try:
            self.lista_clientes_cache = ClienteDAO.obtener_todos()
            self.lista_productos_cache = ProductoDAO.obtener_todos()
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron obtener datos iniciales: {error}")

    def _crear_interfaz_venta(self):
        self.crear_label("Registrar Venta", es_titulo=True)
        frame_cliente = ctk.CTkFrame(self, fg_color="transparent")
        frame_cliente.pack(fill=tk.X, padx=20, pady=5)
        ctk.CTkLabel(frame_cliente, text="Cliente:", text_color=MARRON, font=("Arial", 13, "bold")).pack(
            side=tk.LEFT
        )
        self.opciones_cli = [f"{c[0]} - {c[1]} {c[2]}" for c in self.lista_clientes_cache]
        self.combo_cliente = crear_combo(frame_cliente, self.opciones_cli)
        self.combo_cliente.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        frame_prod = ctk.CTkFrame(self, fg_color=BG_MENU, corner_radius=RADIO)
        frame_prod.pack(fill=tk.X, padx=20, pady=10)
        ctk.CTkLabel(frame_prod, text="Producto:", text_color=MARRON_OSCURO, font=("Arial", 13, "bold")).grid(
            row=0, column=0, sticky="w", padx=15, pady=(10, 0)
        )
        self.opciones_prod = [f"{p[0]} - {p[1]} (Stock: {p[3]})" for p in self.lista_productos_cache]
        self.combo_producto = crear_combo(frame_prod, self.opciones_prod, width=330)
        self.combo_producto.grid(row=1, column=0, padx=15, pady=(2, 12))
        ctk.CTkLabel(frame_prod, text="Cantidad:", text_color=MARRON_OSCURO, font=("Arial", 13, "bold")).grid(
            row=0, column=1, sticky="w", padx=5, pady=(10, 0)
        )
        self.entry_cantidad = ctk.CTkEntry(
            frame_prod, width=80, height=38, corner_radius=RADIO, fg_color="white",
            text_color="black", border_width=0, font=("Arial", 14), justify="center"
        )
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.grid(row=1, column=1, padx=5, pady=(2, 12))
        ctk.CTkButton(
            frame_prod, text="➕ Agregar Item", command=self._agregar_al_carrito,
            width=150, height=38, corner_radius=RADIO, fg_color=MARRON,
            hover_color=MARRON_OSCURO, text_color="white", font=("Arial", 13, "bold")
        ).grid(row=1, column=2, padx=15, pady=(2, 12))

        self.tabla_cart = TablaTarjeta(self, self)
        self.tabla_cart.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.tabla_cart.configurar_columnas([
            ("prod", "Producto", 260, tk.W), ("precio", "P. Unit", 100, tk.E),
            ("cant", "Cant.", 80, tk.CENTER), ("subtotal", "Subtotal", 110, tk.E),
        ])
        frame_pie = ctk.CTkFrame(self, fg_color="transparent")
        frame_pie.pack(fill=tk.X, padx=20, pady=(10, 20))
        self.lbl_total = ctk.CTkLabel(frame_pie, text="Total: $0.00", text_color=MARRON_OSCURO,
                                      font=("Arial", 20, "bold"))
        self.lbl_total.pack(side=tk.LEFT)
        ctk.CTkButton(
            frame_pie, text="✔ Finalizar Venta", command=self.guardar_venta,
            width=190, height=40, corner_radius=RADIO, fg_color=MARRON,
            hover_color=MARRON_OSCURO, text_color="white", font=("Arial", 14, "bold")
        ).pack(side=tk.RIGHT)

    def _agregar_al_carrito(self):
        idx_prod = indice_combo(self.combo_producto, self.opciones_prod)
        if idx_prod == -1:
            messagebox.showerror("Error", "Seleccione un producto válido.")
            return
        try:
            cantidad = int(self.entry_cantidad.get().strip())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un entero mayor a 0.")
            return
        prod_sel = self.lista_productos_cache[idx_prod]
        id_prod, nombre, stock, precio = prod_sel[0], prod_sel[1], prod_sel[3], float(prod_sel[4])
        if cantidad > stock:
            messagebox.showerror("Stock Insuficiente", f"Solo hay {stock} unidades disponibles de {nombre}.")
            return
        subtotal = precio * cantidad
        self.carrito.append({"id_prod": id_prod, "nombre": nombre, "precio": precio,
                             "cantidad": cantidad, "subtotal": subtotal})
        self._actualizar_vista_carrito()

    def _actualizar_vista_carrito(self):
        self.tabla_cart.limpiar()
        total = 0.0
        for item in self.carrito:
            total += item["subtotal"]
            self.tabla_cart.insertar((item["nombre"], f"${item['precio']:.2f}",
                                      item["cantidad"], f"${item['subtotal']:.2f}"))
        self.lbl_total.configure(text=f"Total: ${total:.2f}")

    def guardar_venta(self):
        idx_cli = indice_combo(self.combo_cliente, self.opciones_cli)
        if idx_cli == -1:
            messagebox.showerror("Error", "Seleccione un cliente para la venta.")
            return
        if not self.carrito:
            messagebox.showerror("Error", "El carrito de compras está vacío.")
            return
        id_cliente = self.lista_clientes_cache[idx_cli][0]
        total_venta = sum(item["subtotal"] for item in self.carrito)
        try:
            VentaDAO.procesar_venta(id_cliente, total_venta, self.carrito)
            messagebox.showinfo("Éxito", "Venta registrada e inventario actualizado con éxito.")
            self.destroy()
            self.al_guardar_callback("Ventas")
        except Exception as error:
            messagebox.showerror("Error de Transacción", f"No se pudo completar la venta: {error}")


class VentanaProducto(FormularioBase):
    def __init__(self, parent, al_guardar_callback):
        super().__init__(parent, "Registrar Nuevo Producto", "380x520")
        self.al_guardar_callback = al_guardar_callback
        try:
            self.lista_proveedores_cache = ProveedorDAO.obtener_todos()
        except Exception as error:
            self.lista_proveedores_cache = []
            messagebox.showerror("Error", f"No se pudieron cargar los proveedores: {error}")
        self._crear_interfaz()

    def _crear_interfaz(self):
        self.crear_label("Nuevo Producto", es_titulo=True)
        self.crear_label("Proveedor:")
        self.opciones_prov = [f"{p[0]} - {p[1]}" for p in self.lista_proveedores_cache]
        self.combo_prov = self.crear_combo(self.opciones_prov)
        self.crear_label("Nombre del Producto:")
        self.entry_nombre = self.crear_entrada()
        self.crear_label("Categoría:")
        self.entry_categoria = self.crear_entrada()
        self.crear_label("Precio Actual:")
        self.entry_precio = self.crear_entrada()
        self.crear_label("Stock Inicial:")
        self.entry_stock = self.crear_entrada()
        self.crear_boton("Guardar Producto", self.guardar)

    def guardar(self):
        idx_prov = indice_combo(self.combo_prov, self.opciones_prov)
        nombre, categoria = self.entry_nombre.get().strip(), self.entry_categoria.get().strip()
        precio, stock = self.entry_precio.get().strip(), self.entry_stock.get().strip()
        if idx_prov == -1:
            messagebox.showerror("Error", "Por favor seleccione un proveedor de la lista.")
            return
        if not (nombre and precio and stock):
            messagebox.showerror("Error", "Por favor completa los campos obligatorios.")
            return
        try:
            p_val, s_val = float(precio), int(stock)
            if p_val < 0 or s_val < 0:
                raise ValueError
            ProductoDAO.guardar(self.lista_proveedores_cache[idx_prov][0], nombre, categoria, p_val, s_val)
            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
            self.destroy()
            self.al_guardar_callback("Productos")
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser números válidos mayores o iguales a 0.")
        except Exception as error:
            messagebox.showerror("Error de Base de Datos", f"No se pudo guardar: {error}")


class VentanaProveedor(FormularioBase):
    def __init__(self, parent, al_guardar_callback):
        super().__init__(parent, "Registrar Nuevo Proveedor", "380x450")
        self.al_guardar_callback = al_guardar_callback
        self.crear_label("Nuevo Proveedor", es_titulo=True)
        for etiqueta, atributo in (("Nombre Empresa:", "empresa"), ("Contacto:", "contacto"),
                                   ("Teléfono:", "telefono"), ("Email:", "email")):
            self.crear_label(etiqueta)
            setattr(self, f"entry_{atributo}", self.crear_entrada())
        self.crear_boton("Guardar Proveedor", self.guardar)

    def guardar(self):
        valores = [getattr(self, f"entry_{campo}").get().strip()
                   for campo in ("empresa", "contacto", "telefono", "email")]
        if not valores[0]:
            messagebox.showerror("Error", "El nombre de la empresa es obligatorio.")
            return
        try:
            ProveedorDAO.guardar(*valores)
            messagebox.showinfo("Éxito", "Proveedor guardado correctamente.")
            self.destroy()
            self.al_guardar_callback("Proveedores")
        except Exception as error:
            messagebox.showerror("Error de Base de Datos", f"No se pudo guardar: {error}")


class VentanaCliente(FormularioBase):
    def __init__(self, parent, al_guardar_callback):
        super().__init__(parent, "Registrar Nuevo Cliente", "380x520")
        self.al_guardar_callback = al_guardar_callback
        self.crear_label("Nuevo Cliente", es_titulo=True)
        for etiqueta, atributo in (("Nombre:", "nombre"), ("Apellido:", "apellido"),
                                   ("Correo Electrónico:", "email"), ("Teléfono:", "telefono"),
                                   ("Dirección:", "direccion")):
            self.crear_label(etiqueta)
            setattr(self, f"entry_{atributo}", self.crear_entrada())
        self.crear_boton("Guardar Cliente", self.guardar)

    def guardar(self):
        valores = [getattr(self, f"entry_{campo}").get().strip()
                   for campo in ("nombre", "apellido", "email", "telefono", "direccion")]
        if not (valores[0] and valores[1]):
            messagebox.showerror("Error", "Nombre y Apellido son campos obligatorios.")
            return
        try:
            ClienteDAO.guardar(*valores)
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.destroy()
            self.al_guardar_callback("Clientes")
        except Exception as error:
            messagebox.showerror("Error de Base de Datos", f"No se pudo guardar: {error}")
