import customtkinter as ctk
from tkinter import messagebox
import sqlite3


class AlumnosWindow:

    def __init__(self):

        self.app = ctk.CTkToplevel()

        self.app.title("Gestión de Alumnos")
        self.app.geometry("700x600")

        titulo = ctk.CTkLabel(
            self.app,
            text="Gestión de Alumnos",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        self.nombre = ctk.CTkEntry(
            self.app,
            placeholder_text="Nombre",
            width=300
        )
        self.nombre.pack(pady=5)

        self.apellido = ctk.CTkEntry(
            self.app,
            placeholder_text="Apellido",
            width=300
        )
        self.apellido.pack(pady=5)

        self.edad = ctk.CTkEntry(
            self.app,
            placeholder_text="Edad",
            width=300
        )
        self.edad.pack(pady=5)

        self.telefono = ctk.CTkEntry(
            self.app,
            placeholder_text="Teléfono",
            width=300
        )
        self.telefono.pack(pady=5)

        self.correo = ctk.CTkEntry(
            self.app,
            placeholder_text="Correo",
            width=300
        )
        self.correo.pack(pady=5)

        boton_guardar = ctk.CTkButton(
            self.app,
            text="Guardar Alumno",
            command=self.guardar_alumno
        )
        boton_guardar.pack(pady=20)

    def guardar_alumno(self):

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO alumnos
        (nombre, apellido, edad, telefono, correo)
        VALUES (?, ?, ?, ?, ?)
        """, (
            self.nombre.get(),
            self.apellido.get(),
            self.edad.get(),
            self.telefono.get(),
            self.correo.get()
        ))

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Alumno registrado correctamente"
        )

        self.nombre.delete(0, "end")
        self.apellido.delete(0, "end")
        self.edad.delete(0, "end")
        self.telefono.delete(0, "end")
        self.correo.delete(0, "end")