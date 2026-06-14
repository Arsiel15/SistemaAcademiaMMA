import customtkinter as ctk
from tkinter import messagebox
import sqlite3


class AlumnosWindow:

    def __init__(self):

        self.app = ctk.CTkToplevel()

        self.app.title("Gestión de Alumnos")
        self.app.geometry("700x650")

        # Título
        titulo = ctk.CTkLabel(
            self.app,
            text="Gestión de Alumnos",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        # Nombre
        self.nombre = ctk.CTkEntry(
            self.app,
            placeholder_text="Nombre",
            width=300
        )
        self.nombre.pack(pady=5)

        # Apellido
        self.apellido = ctk.CTkEntry(
            self.app,
            placeholder_text="Apellido",
            width=300
        )
        self.apellido.pack(pady=5)

        # Edad
        self.edad = ctk.CTkEntry(
            self.app,
            placeholder_text="Edad",
            width=300
        )
        self.edad.pack(pady=5)

        # Teléfono
        self.telefono = ctk.CTkEntry(
            self.app,
            placeholder_text="Teléfono",
            width=300
        )
        self.telefono.pack(pady=5)

        # Correo
        self.correo = ctk.CTkEntry(
            self.app,
            placeholder_text="Correo",
            width=300
        )
        self.correo.pack(pady=5)

        # Botón Guardar
        boton_guardar = ctk.CTkButton(
            self.app,
            text="Guardar Alumno",
            command=self.guardar_alumno
        )
        boton_guardar.pack(pady=10)

        # Botón Volver
        boton_volver = ctk.CTkButton(
            self.app,
            text="Volver",
            fg_color="gray",
            hover_color="darkgray",
            command=self.app.destroy
        )
        boton_volver.pack(pady=5)

        self.id_eliminar = ctk.CTkEntry(
            self.app,
            placeholder_text="ID Alumno a eliminar",
            width=300
        )
        self.id_eliminar.pack(pady=5)

        boton_eliminar = ctk.CTkButton(
            self.app,
            text="Eliminar Alumno",
            fg_color="darkred",
            command=self.eliminar_alumno
        )
        boton_eliminar.pack(pady=10)

        # Lista de alumnos
        self.lista_alumnos = ctk.CTkTextbox(
            self.app,
            width=550,
            height=250
        )
        self.lista_alumnos.pack(pady=20)

        self.cargar_alumnos()

    def guardar_alumno(self):

        nombre = self.nombre.get().strip()
        apellido = self.apellido.get().strip()
        edad = self.edad.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()

        # Validar campos vacíos
        if not nombre or not apellido or not edad or not telefono or not correo:
            messagebox.showerror(
                "Error",
                "Todos los campos son obligatorios"
            )
            return

        # Validar edad
        if not edad.isdigit():
            messagebox.showerror(
                "Error",
                "La edad debe ser numérica"
            )
            return

        # Validar teléfono
        if not telefono.isdigit():
            messagebox.showerror(
                "Error",
                "El teléfono solo debe contener números"
            )
            return

        # Validar longitud teléfono
        if len(telefono) != 10:
            messagebox.showerror(
                "Error",
                "El teléfono debe tener 10 dígitos"
            )
            return

        # Validar correo
        if "@" not in correo or "." not in correo:
            messagebox.showerror(
                "Error",
                "Ingrese un correo válido"
            )
            return

        # Guardar en SQLite
        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO alumnos
        (nombre, apellido, edad, telefono, correo)
        VALUES (?, ?, ?, ?, ?)
        """, (
            nombre,
            apellido,
            edad,
            telefono,
            correo
        ))

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Alumno registrado correctamente"
        )

        # Limpiar campos
        self.nombre.delete(0, "end")
        self.apellido.delete(0, "end")
        self.edad.delete(0, "end")
        self.telefono.delete(0, "end")
        self.correo.delete(0, "end")

        # Actualizar lista
        self.cargar_alumnos()



    def cargar_alumnos(self):

        self.lista_alumnos.delete("1.0", "end")

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT id, nombre, apellido, edad, telefono, correo
        FROM alumnos
        ORDER BY id
        """)

        alumnos = cursor.fetchall()

        conexion.close()

        self.lista_alumnos.insert(
            "end",
            "===== ALUMNOS REGISTRADOS =====\n\n"
        )

        if not alumnos:
            self.lista_alumnos.insert(
                "end",
                "No existen alumnos registrados.\n"
            )
            return

        for alumno in alumnos:

            self.lista_alumnos.insert(
                "end",
                f"ID: {alumno[0]}\n"
                f"Nombre: {alumno[1]} {alumno[2]}\n"
                f"Edad: {alumno[3]}\n"
                f"Teléfono: {alumno[4]}\n"
                f"Correo: {alumno[5]}\n"
                f"{'-'*40}\n"
            )

    def eliminar_alumno(self):

        id_alumno = self.id_eliminar.get().strip()

        if not id_alumno.isdigit():

            messagebox.showerror(
                "Error",
                "Ingrese un ID válido"
            )
            return

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM alumnos WHERE id = ?",
            (id_alumno,)
        )

        alumno = cursor.fetchone()

        if not alumno:
            conexion.close()

            messagebox.showerror(
                "Error",
                "No existe un alumno con ese ID"
            )
            return

        cursor.execute(
            "DELETE FROM alumnos WHERE id = ?",
            (id_alumno,)
        )

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Alumno eliminado correctamente"
        )

        self.id_eliminar.delete(0, "end")

        self.cargar_alumnos()