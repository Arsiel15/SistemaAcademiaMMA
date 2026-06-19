import sqlite3


def crear_base_datos():
    conexion = sqlite3.connect("mma.db")
    cursor = conexion.cursor()

    #Tabla usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol TEXT NOT NULL
    )
    """)

    #Tabla alumnos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        edad INTEGER,
        telefono TEXT,
        correo TEXT
    )
    """)

    #Tabla entrenadores

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entrenadores (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        especialidad TEXT,
        telefono TEXT,
        correo TEXT
    )
    """)

    # Tabla pagos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER NOT NULL,
        monto REAL NOT NULL,
        fecha TEXT NOT NULL,
        fecha_vencimiento TEXT NOT NULL,
        concepto TEXT NOT NULL,
        FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asistencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        estado TEXT NOT NULL,
        FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
    )
    """)

    #Usuarios iniciales
    usuarios = [
        ("admin", "admin123", "Administrador"),
        ("recepcion", "recep123", "Recepcionista"),
        ("entrenador", "entre123", "Entrenador")
    ]

    for usuario in usuarios:
        cursor.execute("""
        INSERT OR IGNORE INTO usuarios
        (usuario, password, rol)
        VALUES (?, ?, ?)
        """, usuario)

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_base_datos()
    print("Base de datos creada correctamente")