# File: Datos/acceso_a_datos.py
from Conexion.conexion import ConexionDB


class ProductoDAO:
    """Acceso a datos para la entidad Producto."""

    @staticmethod
    def obtener_todos():
        sql = "SELECT id_producto, nombre, stock, precio_actual FROM producto ORDER BY id_producto ASC"
        try:
            with ConexionDB() as (conexion, cursor):
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"[Error ProductoDAO.obtener_todos]: {e}")
            return []

    @staticmethod
    def guardar(id_prov, nombre, precio, stock):
        sql = "INSERT INTO producto (id_proveedor, nombre, precio_actual, stock) VALUES (%s, %s, %s, %s)"
        with ConexionDB() as (conexion, cursor):
            cursor.execute(sql, (id_prov, nombre, precio, stock))

    @staticmethod
    def eliminar(id_producto):
        """Elimina un producto por su ID."""
        sql = "DELETE FROM producto WHERE id_producto = %s"
        with ConexionDB() as (conexion, cursor):
            cursor.execute(sql, (id_producto,))


class ClienteDAO:
    """Acceso a datos para la entidad Cliente."""

    @staticmethod
    def obtener_todos():
        sql = "SELECT id_cliente, nombre, apellido, email, telefono, direccion FROM cliente ORDER BY id_cliente ASC"
        try:
            with ConexionDB() as (conexion, cursor):
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"[Error ClienteDAO.obtener_todos]: {e}")
            return []

    @staticmethod
    def guardar(nombre, apellido, email, telefono, direccion):
        """Inserta un nuevo cliente en la base de datos."""
        sql = "INSERT INTO cliente (nombre, apellido, email, telefono, direccion) VALUES (%s, %s, %s, %s, %s)"
        with ConexionDB() as (conexion, cursor):
            cursor.execute(sql, (nombre, apellido, email, telefono, direccion))

    @staticmethod
    def eliminar(id_cliente):
        """Elimina un cliente por su ID."""
        sql = "DELETE FROM cliente WHERE id_cliente = %s"
        with ConexionDB() as (conexion, cursor):
            cursor.execute(sql, (id_cliente,))


class ProveedorDAO:
    """Acceso a datos para la entidad Proveedor."""

    @staticmethod
    def obtener_todos():
        sql = "SELECT id_proveedor, nombre_empresa, contacto, telefono, email FROM proveedor ORDER BY id_proveedor ASC"
        try:
            with ConexionDB() as (conexion, cursor):
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"[Error ProveedorDAO.obtener_todos]: {e}")
            return []

    @staticmethod
    def guardar(empresa, contacto, telefono, email):
        sql = "INSERT INTO proveedor (nombre_empresa, contacto, telefono, email) VALUES (%s, %s, %s, %s)"
        with ConexionDB() as (conexion, cursor):
            cursor.execute(sql, (empresa, contacto, telefono, email))

    @staticmethod
    def eliminar(id_proveedor):
        """Elimina un proveedor por su ID."""
        sql = "DELETE FROM proveedor WHERE id_proveedor = %s"
        with ConexionDB() as (conexion, cursor):
            cursor.execute(sql, (id_proveedor,))

class VentaDAO:
    """Acceso a datos para la entidad Venta y sus detalles."""

    @staticmethod
    def obtener_historial():
        sql = """
            SELECT v.id_venta, 
                   CONCAT(c.nombre, ' ', c.apellido) AS cliente, 
                   v.fecha_venta, 
                   v.total
            FROM venta v
            INNER JOIN cliente c ON v.id_cliente = c.id_cliente
            ORDER BY v.fecha_venta DESC
        """
        try:
            with ConexionDB() as (conexion, cursor):
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"[Error VentaDAO.obtener_historial]: {e}")
            return []

    @staticmethod
    def procesar_venta(id_cliente, total_venta, carrito):
        """
        Ejecuta la transacción completa de venta:
        1. Inserta la cabecera en 'venta'.
        2. Obtiene el ID generado.
        3. Inserta los ítems en 'detalle_venta'.
        4. Actualiza el inventario descontando el stock consumido.
        """
        sql_venta = "INSERT INTO venta (id_cliente, fecha_venta, total) VALUES (%s, NOW(), %s)"
        sql_detalle = "INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
        sql_stock = "UPDATE producto SET stock = stock - %s WHERE id_producto = %s"

        with ConexionDB() as (conexion, cursor):
            # 1. Cabecera
            cursor.execute(sql_venta, (id_cliente, total_venta))
            id_venta = cursor.lastrowid

            # 2 y 3. Detalle y Actualización de Stock por ítem
            for item in carrito:
                cursor.execute(sql_detalle, (id_venta, item["id_prod"], item["cantidad"], item["precio"]))
                cursor.execute(sql_stock, (item["cantidad"], item["id_prod"]))