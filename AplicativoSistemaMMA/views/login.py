import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from views.menu import MenuWindow

class LoginWindow:

    def __init__(self):

        self.app = ctk.CTk()

        self.app.title("Sistema MMA")
        self.app.geometry("500x400")

        ctk.set_appearance_mode("dark")

        titulo = ctk.CTkLabel(
            self.app,
            text="Sistema de Gestión MMA",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=30)

        self.usuario_entry = ctk.CTkEntry(
            self.app,
            placeholder_text="Usuario",
            width=250
        )
        self.usuario_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.app,
            placeholder_text="Contraseña",
            show="*",
            width=250
        )
        self.password_entry.pack(pady=10)

        boton_login = ctk.CTkButton(
            self.app,
            text="Ingresar",
            command=self.validar_login
        )
        boton_login.pack(pady=20)

    def validar_login(self):

        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT rol
            FROM usuarios
            WHERE usuario = ?
            AND password = ?
        """, (usuario, password))

        resultado = cursor.fetchone()

        conexion.close()

        if resultado:

            rol = resultado[0]

            self.app.destroy()

            menu = MenuWindow(rol)
            menu.run()

        else:

            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos"
            )

    def run(self):
        self.app.mainloop()