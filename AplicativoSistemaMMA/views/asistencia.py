import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from reportlab.pdfgen import canvas


class AsistenciaWindow:

    def __init__(self):

        self.app = ctk.CTkToplevel()

        self.app.title("Control de Asistencia")
        self.app.geometry("800x800")

        titulo = ctk.CTkLabel(
            self.app,
            text="Control de Asistencia",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        self.alumno_id = ctk.CTkEntry(
            self.app,
            placeholder_text="ID Alumno",
            width=300
        )
        self.alumno_id.pack(pady=10)

        self.estado = ctk.CTkOptionMenu(
            self.app,
            values=["Asistió", "Faltó"]
        )
        self.estado.pack(pady=10)

        boton_registrar = ctk.CTkButton(
            self.app,
            text="Registrar Asistencia",
            command=self.registrar_asistencia
        )
        boton_registrar.pack(pady=10)

        boton_consultar = ctk.CTkButton(
            self.app,
            text="Consultar Alumno",
            command=self.consultar_alumno
        )
        boton_consultar.pack(pady=10)

        boton_todas = ctk.CTkButton(
            self.app,
            text="Ver Todas las Asistencias",
            command=self.cargar_asistencias
        )
        boton_todas.pack(pady=10)

        # ======================
        # REPORTE PDF
        # ======================

        self.id_reporte = ctk.CTkEntry(
            self.app,
            placeholder_text="ID Alumno para Reporte PDF",
            width=300
        )
        self.id_reporte.pack(pady=10)

        boton_pdf = ctk.CTkButton(
            self.app,
            text="Generar Reporte PDF",
            fg_color="green",
            hover_color="darkgreen",
            command=self.generar_reporte_pdf
        )
        boton_pdf.pack(pady=10)

        boton_volver = ctk.CTkButton(
            self.app,
            text="Volver",
            fg_color="gray",
            command=self.app.destroy
        )
        boton_volver.pack(pady=10)

        self.lista = ctk.CTkTextbox(
            self.app,
            width=650,
            height=300
        )
        self.lista.pack(pady=20)

        self.cargar_asistencias()

    def registrar_asistencia(self):

        alumno_id = self.alumno_id.get().strip()

        if not alumno_id.isdigit():

            messagebox.showerror(
                "Error",
                "Ingrese un ID válido"
            )
            return

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM alumnos WHERE id = ?",
            (alumno_id,)
        )

        alumno = cursor.fetchone()

        if not alumno:

            conexion.close()

            messagebox.showerror(
                "Error",
                "Alumno no encontrado"
            )
            return

        fecha = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
        INSERT INTO asistencias
        (alumno_id, fecha, estado)
        VALUES (?, ?, ?)
        """, (
            alumno_id,
            fecha,
            self.estado.get()
        ))

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Asistencia registrada"
        )

        self.cargar_asistencias()

    def consultar_alumno(self):

        alumno_id = self.alumno_id.get().strip()

        if not alumno_id.isdigit():
            return

        self.lista.delete("1.0", "end")

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT
            alumnos.nombre,
            alumnos.apellido,
            asistencias.fecha,
            asistencias.estado
        FROM asistencias
        INNER JOIN alumnos
            ON asistencias.alumno_id = alumnos.id
        WHERE alumnos.id = ?
        ORDER BY asistencias.fecha DESC
        """, (alumno_id,))

        datos = cursor.fetchall()

        conexion.close()

        if not datos:

            self.lista.insert(
                "end",
                "No existen asistencias.\n"
            )
            return

        for fila in datos:

            self.lista.insert(
                "end",
                f"Alumno: {fila[0]} {fila[1]}\n"
                f"Fecha: {fila[2]}\n"
                f"Estado: {fila[3]}\n"
                f"{'-'*40}\n"
            )

    def cargar_asistencias(self):

        self.lista.delete("1.0", "end")

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT
            alumnos.nombre,
            alumnos.apellido,
            asistencias.fecha,
            asistencias.estado
        FROM asistencias
        INNER JOIN alumnos
            ON asistencias.alumno_id = alumnos.id
        ORDER BY asistencias.fecha DESC
        """)

        datos = cursor.fetchall()

        conexion.close()

        self.lista.insert(
            "end",
            "===== ASISTENCIAS =====\n\n"
        )

        if not datos:

            self.lista.insert(
                "end",
                "No existen registros.\n"
            )
            return

        for fila in datos:

            self.lista.insert(
                "end",
                f"Alumno: {fila[0]} {fila[1]}\n"
                f"Fecha: {fila[2]}\n"
                f"Estado: {fila[3]}\n"
                f"{'-'*40}\n"
            )

    def generar_reporte_pdf(self):

        alumno_id = self.id_reporte.get().strip()

        if not alumno_id.isdigit():

            messagebox.showerror(
                "Error",
                "Ingrese un ID válido"
            )
            return

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT nombre, apellido
        FROM alumnos
        WHERE id = ?
        """, (alumno_id,))

        alumno = cursor.fetchone()

        if not alumno:

            conexion.close()

            messagebox.showerror(
                "Error",
                "Alumno no encontrado"
            )
            return

        cursor.execute("""
        SELECT fecha, estado
        FROM asistencias
        WHERE alumno_id = ?
        ORDER BY fecha
        """, (alumno_id,))

        asistencias = cursor.fetchall()

        conexion.close()

        archivo = f"Reporte_Asistencia_{alumno_id}.pdf"

        pdf = canvas.Canvas(archivo)

        pdf.setTitle("Reporte de Asistencia")

        y = 800

        pdf.drawString(
            50,
            y,
            "SISTEMA MMA - REPORTE DE ASISTENCIA"
        )

        y -= 40

        pdf.drawString(
            50,
            y,
            f"Alumno: {alumno[0]} {alumno[1]}"
        )

        y -= 30

        total_asistio = 0
        total_falto = 0

        for asistencia in asistencias:

            pdf.drawString(
                50,
                y,
                f"{asistencia[0]} - {asistencia[1]}"
            )

            if asistencia[1] == "Asistió":
                total_asistio += 1
            else:
                total_falto += 1

            y -= 20

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Total Asistencias: {total_asistio}"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Total Faltas: {total_falto}"
        )

        pdf.save()

        self.id_reporte.delete(0, "end")

        messagebox.showinfo(
            "Éxito",
            f"Reporte generado:\n{archivo}"
        )