CREATE DATABASE IF NOT EXISTS panaderia_cozi;
USE panaderia_cozi;

-- Tabla Proveedor
CREATE TABLE IF NOT EXISTS proveedor (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre_empresa VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(30),
    email VARCHAR(100)
);

-- Tabla Producto
CREATE TABLE IF NOT EXISTS producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    id_proveedor INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio_actual DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor) ON DELETE RESTRICT
);

-- Tabla Cliente
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(30),
    direccion VARCHAR(150)
);

-- Tabla Venta (Encabezado)
CREATE TABLE IF NOT EXISTS venta (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

-- Tabla Detalle Venta
CREATE TABLE IF NOT EXISTS detalle_venta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

-- Datos iniciales de prueba
INSERT INTO proveedor (nombre_empresa, contacto, telefono, email) VALUES 
('Harinas del Sur', 'Juan Pérez', '351-4554321', 'ventas@harinasdelsur.com'),
('Lácteos La Villa', 'Maria Gómez', '351-4889900', 'contacto@lacteoslavilla.com');

INSERT INTO producto (id_proveedor, nombre, precio_actual, stock) VALUES
(1, 'Pan Criollo (kg)', 1800.00, 45),
(1, 'Facturas surtidas (docena)', 4200.00, 20),
(2, 'Torta Selva Negra', 15000.00, 3);

INSERT INTO cliente (nombre, apellido, email, telefono, direccion) VALUES 
('Carlos', 'López', 'carlos.lopez@email.com', '351-6112233', 'Av. Colón 1234'),
('Ana', 'Martínez', 'ana.m@email.com', '351-7445566', 'Calle Jujuy 432');