import customtkinter as ctk
from tkinter import messagebox
import sqlite3


class EntrenadoresWindow:

    def __init__(self):

        self.app = ctk.CTkToplevel()

        self.app.title("Gestión de Entrenadores")
        self.app.geometry("750x800")

        # Título
        titulo = ctk.CTkLabel(
            self.app,
            text="Gestión de Entrenadores",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        # Contador
        self.lbl_total = ctk.CTkLabel(
            self.app,
            text="Total entrenadores registrados: 0",
            font=("Arial", 14, "bold")
        )
        self.lbl_total.pack(pady=5)

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

        # Especialidad
        self.especialidad = ctk.CTkEntry(
            self.app,
            placeholder_text="Especialidad",
            width=300
        )
        self.especialidad.pack(pady=5)

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

        # Guardar
        boton_guardar = ctk.CTkButton(
            self.app,
            text="Guardar Entrenador",
            command=self.guardar_entrenador
        )
        boton_guardar.pack(pady=10)

        # Volver
        boton_volver = ctk.CTkButton(
            self.app,
            text="Volver",
            fg_color="gray",
            hover_color="darkgray",
            command=self.app.destroy
        )
        boton_volver.pack(pady=5)

        # Eliminar
        self.id_eliminar = ctk.CTkEntry(
            self.app,
            placeholder_text="ID Entrenador a eliminar",
            width=300
        )
        self.id_eliminar.pack(pady=5)

        boton_eliminar = ctk.CTkButton(
            self.app,
            text="Eliminar Entrenador",
            fg_color="darkred",
            hover_color="#8B0000",
            command=self.eliminar_entrenador
        )
        boton_eliminar.pack(pady=10)

        # Editar
        self.id_editar = ctk.CTkEntry(
            self.app,
            placeholder_text="ID Entrenador a editar",
            width=300
        )
        self.id_editar.pack(pady=5)

        boton_editar = ctk.CTkButton(
            self.app,
            text="Actualizar Entrenador",
            fg_color="green",
            hover_color="darkgreen",
            command=self.editar_entrenador
        )
        boton_editar.pack(pady=10)

        # Buscar
        self.buscar_nombre = ctk.CTkEntry(
            self.app,
            placeholder_text="Buscar por nombre",
            width=300
        )
        self.buscar_nombre.pack(pady=5)

        boton_buscar = ctk.CTkButton(
            self.app,
            text="Buscar Entrenador",
            command=self.buscar_entrenador
        )
        boton_buscar.pack(pady=5)

        boton_mostrar_todos = ctk.CTkButton(
            self.app,
            text="Mostrar Todos",
            command=self.cargar_entrenadores
        )
        boton_mostrar_todos.pack(pady=5)

        # Lista
        self.lista_entrenadores = ctk.CTkTextbox(
            self.app,
            width=600,
            height=250
        )
        self.lista_entrenadores.pack(pady=20)

        self.cargar_entrenadores()

    def guardar_entrenador(self):

        nombre = self.nombre.get().strip()
        apellido = self.apellido.get().strip()
        especialidad = self.especialidad.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()

        if not nombre or not apellido or not especialidad or not telefono or not correo:
            messagebox.showerror(
                "Error",
                "Todos los campos son obligatorios"
            )
            return

        if not telefono.isdigit():
            messagebox.showerror(
                "Error",
                "El teléfono solo debe contener números"
            )
            return

        if len(telefono) != 10:
            messagebox.showerror(
                "Error",
                "El teléfono debe tener 10 dígitos"
            )
            return

        if "@" not in correo or "." not in correo:
            messagebox.showerror(
                "Error",
                "Ingrese un correo válido"
            )
            return

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT *
        FROM entrenadores
        WHERE nombre = ?
        AND apellido = ?
        AND telefono = ?
        """, (
            nombre,
            apellido,
            telefono
        ))

        existe = cursor.fetchone()

        if existe:
            conexion.close()

            messagebox.showerror(
                "Error",
                "El entrenador ya se encuentra registrado"
            )
            return

        cursor.execute("""
        INSERT INTO entrenadores
        (nombre, apellido, especialidad, telefono, correo)
        VALUES (?, ?, ?, ?, ?)
        """, (
            nombre,
            apellido,
            especialidad,
            telefono,
            correo
        ))

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Entrenador registrado correctamente"
        )

        self.nombre.delete(0, "end")
        self.apellido.delete(0, "end")
        self.especialidad.delete(0, "end")
        self.telefono.delete(0, "end")
        self.correo.delete(0, "end")

        self.cargar_entrenadores()

    def cargar_entrenadores(self):

        self.lista_entrenadores.delete("1.0", "end")

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT id, nombre, apellido, especialidad, telefono, correo
        FROM entrenadores
        ORDER BY id
        """)

        entrenadores = cursor.fetchall()

        conexion.close()

        self.lbl_total.configure(
            text=f"Total entrenadores registrados: {len(entrenadores)}"
        )

        self.lista_entrenadores.insert(
            "end",
            "===== ENTRENADORES REGISTRADOS =====\n\n"
        )

        if not entrenadores:
            self.lista_entrenadores.insert(
                "end",
                "No existen entrenadores registrados.\n"
            )
            return

        for entrenador in entrenadores:

            self.lista_entrenadores.insert(
                "end",
                f"ID: {entrenador[0]}\n"
                f"Nombre: {entrenador[1]} {entrenador[2]}\n"
                f"Especialidad: {entrenador[3]}\n"
                f"Teléfono: {entrenador[4]}\n"
                f"Correo: {entrenador[5]}\n"
                f"{'-'*40}\n"
            )

    def buscar_entrenador(self):

        nombre_busqueda = self.buscar_nombre.get().strip()

        if not nombre_busqueda:
            self.cargar_entrenadores()
            return

        self.lista_entrenadores.delete("1.0", "end")

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT id, nombre, apellido, especialidad, telefono, correo
        FROM entrenadores
        WHERE nombre LIKE ?
        ORDER BY id
        """, (f"%{nombre_busqueda}%",))

        entrenadores = cursor.fetchall()

        conexion.close()

        if not entrenadores:
            self.lista_entrenadores.insert(
                "end",
                "No se encontraron entrenadores."
            )
            return

        for entrenador in entrenadores:

            self.lista_entrenadores.insert(
                "end",
                f"ID: {entrenador[0]}\n"
                f"Nombre: {entrenador[1]} {entrenador[2]}\n"
                f"Especialidad: {entrenador[3]}\n"
                f"Teléfono: {entrenador[4]}\n"
                f"Correo: {entrenador[5]}\n"
                f"{'-'*40}\n"
            )

    def editar_entrenador(self):

        id_entrenador = self.id_editar.get().strip()

        if not id_entrenador.isdigit():
            messagebox.showerror(
                "Error",
                "Ingrese un ID válido"
            )
            return

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        UPDATE entrenadores
        SET nombre = ?,
            apellido = ?,
            especialidad = ?,
            telefono = ?,
            correo = ?
        WHERE id = ?
        """, (
            self.nombre.get(),
            self.apellido.get(),
            self.especialidad.get(),
            self.telefono.get(),
            self.correo.get(),
            id_entrenador
        ))

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Entrenador actualizado correctamente"
        )

        self.cargar_entrenadores()

    def eliminar_entrenador(self):

        id_entrenador = self.id_eliminar.get().strip()

        if not id_entrenador.isdigit():
            messagebox.showerror(
                "Error",
                "Ingrese un ID válido"
            )
            return

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM entrenadores WHERE id = ?",
            (id_entrenador,)
        )

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Entrenador eliminado correctamente"
        )

        self.id_eliminar.delete(0, "end")

        self.cargar_entrenadores()