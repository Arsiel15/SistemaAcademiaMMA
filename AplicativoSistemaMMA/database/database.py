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