**Diccionario de Entidades**

* CLIENTE: id\_cliente (PK), nombre, apellido, email, telefono, direccion, fecha\_registro  
    
* PROVEEDOR: id\_proveedor (PK), nombre\_proveedor, contacto, telefono, email  
    
* PRODUCTO: id\_producto (PK), id\_proveedor (FK), nombre, precio\_actual, stock
    
* VENTA: id\_venta (PK), id\_cliente (FK), fecha\_venta, total  
    
* DETALLE\_VENTA: id\_detalle (PK), id\_venta (FK), id\_producto (FK), cantidad, precio\_unitario, subtotal  
    
* HISTORIAL\_PRECIO: id\_historial\_precio (PK), id\_producto (FK), precio\_anterior, precio\_nuevo, fecha\_cambio  
    
* HISTORIAL\_VENTA: id\_historial\_venta (PK), id\_venta (FK), estado\_venta, fecha\_registro, observaciones

**Script SQL (DDL)**

\-- 1\. Tabla: Proveedor  
CREATE TABLE proveedor (  
    id\_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,  
    nombre\_proveedor VARCHAR(150) NOT NULL,  
    contacto VARCHAR(100),  
    telefono VARCHAR(20),  
    email VARCHAR(150) UNIQUE  
);

\-- 2\. Tabla: Cliente  
CREATE TABLE cliente (  
    id\_cliente INTEGER PRIMARY KEY AUTOINCREMENT,  
    nombre VARCHAR(100) NOT NULL,  
    apellido VARCHAR(100) NOT NULL,  
    email VARCHAR(150) UNIQUE,  
    telefono VARCHAR(20),  
    direccion TEXT,  
    fecha\_registro TIMESTAMP DEFAULT CURRENT\_TIMESTAMP NOT NULL  
);

\-- 3\. Tabla: Producto  
CREATE TABLE producto (  
    id\_producto INTEGER PRIMARY KEY AUTOINCREMENT,  
    id\_proveedor INTEGER NOT NULL,  
    nombre VARCHAR(150) NOT NULL,  
    precio\_actual DECIMAL(10,2) NOT NULL CHECK (precio\_actual \> 0),  
    stock INTEGER NOT NULL CHECK (stock \>= 0),  
    CONSTRAINT fk\_producto\_proveedor   
        FOREIGN KEY (id\_proveedor)   
        REFERENCES proveedor(id\_proveedor)   
        ON DELETE RESTRICT  
);

\-- 4\. Tabla: Historial de Precio  
CREATE TABLE historial\_precio (  
    id\_historial\_precio INTEGER PRIMARY KEY AUTOINCREMENT,  
    id\_producto INTEGER NOT NULL,  
    precio\_anterior DECIMAL(10,2) NOT NULL,  
    precio\_nuevo DECIMAL(10,2) NOT NULL,  
    fecha\_cambio TIMESTAMP DEFAULT CURRENT\_TIMESTAMP NOT NULL,  
    CONSTRAINT fk\_historial\_producto   
        FOREIGN KEY (id\_producto)   
        REFERENCES producto(id\_producto)   
        ON DELETE CASCADE  
);

\-- 5\. Tabla: Venta  
CREATE TABLE venta (  
    id\_venta INTEGER PRIMARY KEY AUTOINCREMENT,  
    id\_cliente INTEGER NOT NULL,  
    fecha\_venta TIMESTAMP DEFAULT CURRENT\_TIMESTAMP NOT NULL,  
    total DECIMAL(12,2) DEFAULT 0.00 NOT NULL,  
    CONSTRAINT fk\_venta\_cliente   
        FOREIGN KEY (id\_cliente)   
        REFERENCES cliente(id\_cliente)   
        ON DELETE RESTRICT  
);

\-- 6\. Tabla: Detalle de Venta  
CREATE TABLE detalle\_venta (  
    id\_detalle INTEGER PRIMARY KEY AUTOINCREMENT,  
    id\_venta INTEGER NOT NULL,  
    id\_producto INTEGER NOT NULL,  
    cantidad INTEGER NOT NULL CHECK (cantidad \> 0),  
    precio\_unitario DECIMAL(10,2) NOT NULL CHECK (precio\_unitario \> 0),  
    subtotal DECIMAL(12,2) NOT NULL,  
    CONSTRAINT fk\_detalle\_venta   
        FOREIGN KEY (id\_venta)   
        REFERENCES venta(id\_venta)   
        ON DELETE CASCADE,  
    CONSTRAINT fk\_detalle\_producto   
        FOREIGN KEY (id\_producto)   
        REFERENCES producto(id\_producto)   
        ON DELETE RESTRICT  
);

\-- 7\. Tabla: Historial de Venta  
CREATE TABLE historial\_venta (  
    id\_historial\_venta INTEGER PRIMARY KEY AUTOINCREMENT,  
    id\_venta INTEGER NOT NULL,  
    estado\_venta VARCHAR(50) NOT NULL,  
    fecha\_registro TIMESTAMP DEFAULT CURRENT\_TIMESTAMP NOT NULL,  
    observaciones TEXT,  
    CONSTRAINT fk\_historial\_venta   
        FOREIGN KEY (id\_venta)   
        REFERENCES venta(id\_venta)   
        ON DELETE CASCADE  
);  
