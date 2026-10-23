"""Componentes y utilidades visuales reutilizables."""

import tkinter as tk
from tkinter import ttk

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps, ImageTk

from .config import (
    ANCHO_SCROLL,
    BG,
    MARRON,
    MARRON_OSCURO,
    PLACEHOLDER_COMBO,
    RADIO,
    RADIO_CARD,
    RUTA_LOGO,
    TAMANO_LOGO,
    TEXTO,
    SCROLL_MARGEN,
)


def cargar_logo():
    """Devuelve el logo escalado o None cuando el archivo no está disponible."""
    try:
        img = Image.open(RUTA_LOGO).convert("RGBA")
    except (FileNotFoundError, OSError):
        return None

    ancho, alto = img.size
    escala = min(TAMANO_LOGO[0] / ancho, TAMANO_LOGO[1] / alto)
    tamano = (max(1, int(ancho * escala)), max(1, int(alto * escala)))
    return ctk.CTkImage(light_image=img, dark_image=img, size=tamano)


def configurar_estilos():
    """Configura la apariencia de las tablas ttk."""
    style = ttk.Style()
    style.theme_use("clam")
    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold"),
        background=MARRON,
        foreground="white",
        relief="flat",
        padding=6,
    )
    style.map("Treeview.Heading", background=[("active", MARRON)])
    style.configure(
        "Treeview",
        font=("Arial", 10),
        rowheight=28,
        background="white",
        fieldbackground="white",
        foreground=TEXTO,
        borderwidth=0,
    )
    style.map("Treeview", background=[("selected", MARRON)], foreground=[("selected", "white")])


def crear_combo(parent, opciones, **kwargs):
    """Crea un combo con el estilo común y un valor inicial neutro."""
    combo = ctk.CTkComboBox(
        parent,
        values=opciones,
        state="readonly",
        height=38,
        corner_radius=RADIO,
        border_width=0,
        fg_color="white",
        text_color="black",
        button_color=MARRON,
        button_hover_color=MARRON_OSCURO,
        dropdown_fg_color="white",
        dropdown_text_color="black",
        dropdown_hover_color=BG,
        font=("Arial", 14),
        dropdown_font=("Arial", 13),
        **kwargs,
    )
    combo.set(PLACEHOLDER_COMBO)
    return combo


def indice_combo(combo, opciones):
    """Devuelve el índice seleccionado o -1 si sigue en el placeholder."""
    try:
        return opciones.index(combo.get())
    except ValueError:
        return -1


class TablaTarjeta:
    """Tabla ttk dentro de una tarjeta blanca con scroll y encabezado redondeado."""

    def __init__(self, parent, ventana):
        self.ventana = ventana
        try:
            self.escala = ctk.ScalingTracker.get_window_scaling(ventana)
        except (AttributeError, tk.TclError):
            self.escala = 1.0
        self.ancho_relleno = int(24 * self.escala)
        self.radio_px = max(8, round(RADIO_CARD * self.escala))

        self.frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=RADIO_CARD)
        self.tabla = ttk.Treeview(self.frame, show="headings")
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))

        self.barra_scroll = tk.Frame(self.frame, bg="white", bd=0, highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(
            self.barra_scroll,
            orientation="vertical",
            width=ANCHO_SCROLL,
            command=self.tabla.yview,
            button_color=MARRON,
            button_hover_color=MARRON_OSCURO,
        )
        self.scrollbar.pack(fill=tk.Y, expand=True)
        self.tabla.configure(yscrollcommand=self.scrollbar.set)

        self._crear_esquina_header("izquierda")
        self._crear_esquina_header("derecha")
        ventana.after(200, self._posicionar_scroll)
        ventana.after(800, self._posicionar_scroll)

    def _posicionar_scroll(self):
        try:
            self.ventana.update_idletasks()
            alto = 0
            for y in range(150):
                if self.tabla.identify("region", 20, y) not in ("heading", "separator"):
                    break
                alto = y + 1
            if alto < 10:
                alto = int(32 * self.escala)
            inicio = alto + SCROLL_MARGEN
            self.barra_scroll.place(
                in_=self.tabla,
                relx=1.0,
                x=-int(5 * self.escala),
                y=inicio,
                anchor="ne",
                width=int(ANCHO_SCROLL * self.escala) + 4,
                relheight=1.0,
                height=-(inicio + int(6 * self.escala)),
            )
        except tk.TclError:
            pass

    def _crear_esquina_header(self, lado):
        escala = self.radio_px * 8
        img = Image.new("RGB", (escala * 2, escala * 2), BG)
        ImageDraw.Draw(img).ellipse((0, 0, escala * 2 - 1, escala * 2 - 1), fill=MARRON)
        esquina = img.crop((0, 0, escala, escala)).resize(
            (self.radio_px, self.radio_px), Image.Resampling.LANCZOS
        )
        if lado == "derecha":
            esquina = ImageOps.mirror(esquina)
        foto = ImageTk.PhotoImage(esquina)
        etiqueta = tk.Label(self.frame, image=foto, bd=0, highlightthickness=0, bg=BG)
        etiqueta.image = foto
        if lado == "izquierda":
            etiqueta.place(in_=self.tabla, x=0, y=0)
        else:
            etiqueta.place(in_=self.tabla, relx=1.0, x=0, y=0, anchor="ne")

    def configurar_columnas(self, configuraciones):
        self.tabla["columns"] = tuple(c[0] for c in configuraciones) + ("_relleno",)
        for col, cabecera, ancho, alineacion in configuraciones:
            self.tabla.heading(col, text=cabecera)
            self.tabla.column(col, width=ancho, anchor=alineacion)
        self.tabla.heading("_relleno", text="")
        self.tabla.column(
            "_relleno",
            width=self.ancho_relleno,
            minwidth=self.ancho_relleno,
            stretch=False,
        )

    def limpiar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

    def insertar(self, valores):
        self.tabla.insert("", tk.END, values=valores)

    def valores_seleccionados(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        return self.tabla.item(seleccion[0], "values")
