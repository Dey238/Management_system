"""Ventana principal y navegación entre módulos."""

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from Datos.acceso_a_datos import ClienteDAO, ProductoDAO, ProveedorDAO, VentaDAO

from .componentes import TablaTarjeta, cargar_logo, configurar_estilos
from .config import BG, BG_MENU, MARRON, MARRON_HOVER, MARRON_OSCURO, RADIO, ROJO, ROJO_HOVER
from .formularios import VentanaCliente, VentanaNuevaVenta, VentanaProducto, VentanaProveedor


class SistemaPanaderia:
    """Controla la ventana principal, el menú y las tablas de cada módulo."""

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Ventas - Panadería Cozi")
        self.root.geometry("1100x600")
        self.root.configure(fg_color=BG)
        configurar_estilos()
        self.botones_menu = {}
        self._crear_interfaz()
        self.cambiar_modulo("Productos")

    def _crear_interfaz(self):
        frame_menu = ctk.CTkFrame(self.root, width=220, corner_radius=0, fg_color=BG_MENU)
        frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        frame_menu.pack_propagate(False)

        self.imagen_logo = cargar_logo()
        if self.imagen_logo:
            ctk.CTkLabel(frame_menu, image=self.imagen_logo, text="").pack(pady=(25, 20))
        else:
            ctk.CTkLabel(
                frame_menu, text="PANADERÍA COZI", text_color=MARRON_OSCURO,
                font=("Arial", 16, "bold")
            ).pack(pady=25)

        for texto, nombre in (
            ("📦 Productos", "Productos"),
            ("🛒 Ventas", "Ventas"),
            ("👥 Clientes", "Clientes"),
            ("🚚 Proveedores", "Proveedores"),
        ):
            boton = ctk.CTkButton(
                frame_menu,
                text=texto,
                command=lambda modulo=nombre: self.cambiar_modulo(modulo),
                height=38,
                corner_radius=RADIO,
                fg_color=MARRON,
                hover_color=MARRON_HOVER,
                text_color="white",
                font=("Arial", 14, "bold"),
                anchor="w",
            )
            boton.pack(fill=tk.X, padx=15, pady=5)
            self.botones_menu[nombre] = boton

        frame_trabajo = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_trabajo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        frame_superior = ctk.CTkFrame(frame_trabajo, fg_color="transparent")
        frame_superior.pack(fill=tk.X, padx=30, pady=20)
        self.label_titulo = ctk.CTkLabel(
            frame_superior, text="", text_color=MARRON_OSCURO, font=("Arial", 24, "bold")
        )
        self.label_titulo.pack(side=tk.LEFT)
        self.frame_acciones = ctk.CTkFrame(frame_superior, fg_color="transparent")
        self.frame_acciones.pack(side=tk.RIGHT)
        self.tabla = TablaTarjeta(frame_trabajo, self.root)
        self.tabla.frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))

    def _crear_boton_accion(self, texto, comando, color=MARRON, color_hover=MARRON_OSCURO):
        ctk.CTkButton(
            self.frame_acciones, text=texto, command=comando, height=36, corner_radius=RADIO,
            fg_color=color, hover_color=color_hover, text_color="white",
            font=("Arial", 13, "bold")
        ).pack(side=tk.LEFT, padx=5)

    def cambiar_modulo(self, nombre_modulo):
        self.label_titulo.configure(text=f"Módulo de {nombre_modulo}")
        for nombre, boton in self.botones_menu.items():
            boton.configure(fg_color=MARRON_OSCURO if nombre == nombre_modulo else MARRON)
        for widget in self.frame_acciones.winfo_children():
            widget.destroy()
        self.tabla.limpiar()
        cargadores = {
            "Productos": self._cargar_modulo_productos,
            "Ventas": self._cargar_modulo_ventas,
            "Clientes": self._cargar_modulo_clientes,
            "Proveedores": self._cargar_modulo_proveedores,
        }
        cargadores[nombre_modulo]()

    def _cargar_modulo_productos(self):
        self._crear_boton_accion(
            "+ Nuevo Producto", lambda: VentanaProducto(self.root, self.cambiar_modulo)
        )
        self._crear_boton_accion(
            "🗑 Eliminar Producto", self._eliminar_producto, ROJO, ROJO_HOVER
        )
        self.tabla.configurar_columnas([
            ("codigo", "Código", 80, tk.CENTER), ("nombre", "Producto", 250, tk.W),
            ("categoria", "Categoría", 150, tk.W), ("stock", "Stock", 90, tk.CENTER),
            ("precio", "Precio", 110, tk.E),
        ])
        for producto in ProductoDAO.obtener_todos():
            self.tabla.insertar(producto)

    def _eliminar_producto(self):
        valores = self.tabla.valores_seleccionados()
        if not valores:
            messagebox.showwarning("Atención", "Por favor, seleccione un producto de la tabla para eliminar.")
            return
        if not messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar el producto '{valores[1]}' (Código: {valores[0]})?",
        ):
            return
        try:
            ProductoDAO.eliminar(valores[0])
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            self.cambiar_modulo("Productos")
        except Exception as error:
            messagebox.showerror(
                "Error de Base de Datos",
                "No se pudo eliminar el producto. Si ya está registrado en alguna venta, "
                f"la base de datos impedirá la eliminación.\nDetalle: {error}",
            )

    def _cargar_modulo_ventas(self):
        self._crear_boton_accion(
            "+ Procesar Venta", lambda: VentanaNuevaVenta(self.root, self.cambiar_modulo)
        )
        self.tabla.configurar_columnas([
            ("id_venta", "Nº Venta", 90, tk.CENTER), ("cliente", "Cliente", 250, tk.W),
            ("fecha", "Fecha / Hora", 180, tk.CENTER), ("total", "Total ($)", 120, tk.E),
        ])
        try:
            for venta in VentaDAO.obtener_historial():
                self.tabla.insertar((venta[0], venta[1], venta[2], f"${float(venta[3]):.2f}"))
        except Exception as error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar las ventas: {error}")

    def _cargar_modulo_clientes(self):
        self._crear_boton_accion(
            "+ Nuevo Cliente", lambda: VentanaCliente(self.root, self.cambiar_modulo)
        )
        self._crear_boton_accion("🗑 Eliminar Cliente", self._eliminar_cliente, ROJO, ROJO_HOVER)
        self.tabla.configurar_columnas([
            ("id", "ID", 50, tk.CENTER), ("nombre", "Nombre", 120, tk.W),
            ("apellido", "Apellido", 120, tk.W), ("email", "Correo Electrónico", 180, tk.W),
            ("telefono", "Teléfono", 100, tk.CENTER), ("direccion", "Dirección", 180, tk.W),
        ])
        for cliente in ClienteDAO.obtener_todos():
            self.tabla.insertar(cliente)

    def _eliminar_cliente(self):
        valores = self.tabla.valores_seleccionados()
        if not valores:
            messagebox.showwarning("Atención", "Por favor, seleccione un cliente de la tabla para eliminar.")
            return
        nombre = f"{valores[1]} {valores[2]}"
        if not messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al cliente '{nombre}' (ID: {valores[0]})?",
        ):
            return
        try:
            ClienteDAO.eliminar(valores[0])
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            self.cambiar_modulo("Clientes")
        except Exception as error:
            messagebox.showerror(
                "Error de Base de Datos",
                f"No se pudo eliminar el cliente. Si tiene ventas registradas, no se puede eliminar.\nDetalle: {error}",
            )

    def _cargar_modulo_proveedores(self):
        self._crear_boton_accion(
            "+ Nuevo Proveedor", lambda: VentanaProveedor(self.root, self.cambiar_modulo)
        )
        self._crear_boton_accion("🗑 Eliminar Proveedor", self._eliminar_proveedor, ROJO, ROJO_HOVER)
        self.tabla.configurar_columnas([
            ("id", "Código", 70, tk.CENTER), ("empresa", "Empresa", 200, tk.W),
            ("contacto", "Contacto", 150, tk.W), ("telefono", "Teléfono", 120, tk.CENTER),
            ("email", "Correo Electrónico", 200, tk.W),
        ])
        for proveedor in ProveedorDAO.obtener_todos():
            self.tabla.insertar(proveedor)

    def _eliminar_proveedor(self):
        valores = self.tabla.valores_seleccionados()
        if not valores:
            messagebox.showwarning("Atención", "Por favor, seleccione un proveedor de la tabla para eliminar.")
            return
        if not messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al proveedor '{valores[1]}' (Código: {valores[0]})?",
        ):
            return
        try:
            ProveedorDAO.eliminar(valores[0])
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
            self.cambiar_modulo("Proveedores")
        except Exception as error:
            messagebox.showerror(
                "Error de Base de Datos",
                "No se pudo eliminar el proveedor. Si tiene productos asociados, "
                f"la base de datos impedirá la eliminación.\nDetalle: {error}",
            )


def iniciar_interfaz():
    """Punto de entrada de la aplicación autenticada."""
    root = ctk.CTk()
    SistemaPanaderia(root)
    root.mainloop()
