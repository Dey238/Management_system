# Sistema de gestion Panaderia Cozi
Diseño e implementación de una aplicación de gestión para la PyME "Panadería Cozi", optimizando el inventario, la gestión de ventas y la reposición de stock desarrollada para la Tecnicatura Superior en Desarrollo de Software del ISPC.

**PROGRAMACIÓN Y BASE DE DATOS** - **MÓDULO PROGRAMADOR**  

**PROFESORES:** 
- Maria Florencia Garcia Zavia  
- Enzo Eduardo Bruno
  
**CICLO LECTIVO:** 2026  

### INTEGRANTES Y ROLES:
* **Coordinador:** Rodriguez Sofia Belen 
* **Modelo de datos:** Machado Rebeca Anahi, Miranda Nicolas
* **Interfaz:** Puntano Ezequiel 
* **Acceso a datos:** Parra Alexander 
* **Validaciones:** Tula Emiliano
* **Documentación y pruebas:** Molina Ricardo

---

## 📦 ENTIDADES DEL SISTEMA

* **Producto:** Representa el catálogo y el control de inventario.
* **Venta:** Registro de cada transacción realizada.
* **Detalle_venta:** Entidad intermedia para permitir vender varios productos en una sola venta.
* **Cliente:** Registro de clientes recurrentes.
* **Proveedor:** Representa la reposición de stock de los productos finales.
* **Historial_Precio:** Entidad para guardar históricos de cambios en los precios.


---

## 💻 INTERFAZ Y BOCETOS

**Bocetos de pantallas:** [Enlace](https://drive.google.com/file/d/1Nx_9Q5KZE8eGQSQ4LkN_1-m_OVoIoPfT/view?usp=sharing "Enlace")

**Breve explicación del funcionamiento:**
* **Pantalla dividida en dos:**
  * **Izquierda:** Menú con botones para moverse entre: Productos, Ventas, Clientes, Proveedores y Reportes.
  * **Derecha:** Muestra la pantalla del módulo en el que estés (ej. la lista de productos).
* **Pantalla de Productos:**
  * Tiene un título, un botón para agregar nuevo producto, una barra para buscar y un filtro por categoría.
  * Muestra una tabla con: Código, Producto, Stock y Precio.
  * Abajo tiene botones para Editar o Eliminar el producto que selecciones en la tabla.
* **Tecnología:** Se usa la librería **Tkinter** (Python).
  * La ventana principal tiene funciones para armar el menú, el panel de productos y cargar datos de prueba. Los demás botones por el momento imprimen mensajes en consola para probar su interactividad.

---
## Tecnologías

- Python 3.11+
- customtkinter
- Pillow (PIL)
- MySQL 8.0+
- mysql-connector-python

---
## Estructura

```text
PyME_Panaderia_Cozi/
├── Interfaz/
│   ├── config.py
│   ├── componentes.py
│   ├── formularios.py
│   ├── ventana_principal.py
│   ├── interfaz.py
│   └── login.py
├── Datos/
│   ├── acceso_a_datos.py
└── Conexion/
│   ├── conexion.py
├── main.py
├── README.md
```

La interfaz está organizada por responsabilidades: `config.py` centraliza la
configuración visual, `componentes.py` contiene widgets reutilizables,
`formularios.py` contiene las ventanas modales y `ventana_principal.py`
gestiona la navegación y los módulos. `interfaz.py` se conserva como punto de
entrada compatible.

---
## REQUISITOS PREVIOS

Antes de ejecutar el proyecto, asegurate de tener instalado:

1. Python 3.11 o superior - https://www.python.org/downloads/
2. MySQL Server 8.0 o superior - https://dev.mysql.com/downloads/mysql/
3. Microsoft Visual C++ Redistributable (x64) - https://aka.ms/vs/17/release/vc_redist.x64.exe
   (Necesario para que MySQL funcione en Windows)
4. Git - https://git-scm.com/downloads

Verificar instalaciones:

    python --version       (debe mostrar 3.11 o superior)
    git --version

Para verificar MySQL, abrí una terminal y ejecutá:

    mysql --version

Si dice "command not found" o "no se reconoce", hay que agregar MySQL al PATH.

## CÓMO PROBAR EL PROYECTO

1. Clonar el repositorio:

    git clone https://github.com/ricardoalbertomolina/PyME_Panaderia_Cozi.git
    cd PyME_Panaderia_Cozi

2. Crear y activar un entorno virtual:

    Windows (PowerShell):
        python -m venv venv
        venv\Scripts\Activate.ps1

    Windows (Git Bash):
        python -m venv venv
        source venv/Scripts/activate

   Una vez activado, el prompt debe empezar con (venv).

3. Instalar dependencias:

    pip install -r requirements.txt

4. Crear la base de datos:

    Iniciá el servicio de MySQL y luego ejecutá el script del proyecto.

    Iniciar MySQL (Windows):
        Start-Service MySQL267

    Ejecutar el script SQL:

    Desde Git Bash:
        mysql -u root -p < Documentacion/schema.sql

    Desde PowerShell (Windows):
        Get-Content Documentacion\schema.sql | & "C:\Program Files\MySQL\MySQL Server 26.7\bin\mysql.exe" -u root -p

    Nota: si el script se ejecuta dos veces seguidas, la segunda dará error por duplicados.
    En ese caso, primero ejecutar:
        DROP DATABASE IF EXISTS panaderia_cozi;
    Y luego volver a correr el script.

5. Configurar credenciales de MySQL:

    Abrí Conexion/conexion.py y reemplazá el valor por defecto:

        "password": os.getenv("DB_PASSWORD", "TU_CONTRASEÑA"),

    Cambialo por tu contraseña real de MySQL:

        "password": os.getenv("DB_PASSWORD", "tu_contraseña_real"),

    Alternativa (recomendada): usar variables de entorno sin editar el código:

    PowerShell (Windows):
        $env:DB_PASSWORD = "tu_contraseña_real"
        python main.py

    Git Bash:
        export DB_PASSWORD="tu_contraseña_real"
        python main.py

6. Verificar la conexión:

    python -c "from Conexion.conexion import conectar; c = conectar(); print('OK' if c else 'FALLO'); c.close() if c else None"

    Debe imprimir OK.

7. Ejecutar la aplicación:

    python main.py

8. Iniciar sesión:

    Credenciales de prueba:
        Usuario:    panaderia
        Contraseña: 1234

    Aclaración: las credenciales están actualmente hardcodeadas en Interfaz/login.py.
    No se validan contra la base de datos. Es una mejora pendiente.

