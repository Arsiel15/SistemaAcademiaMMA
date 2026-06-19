import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class PagosWindow:

    def __init__(self):

        self.app = ctk.CTkToplevel()

        self.app.title("Gestión de Pagos")
        self.app.geometry("800x800")

        titulo = ctk.CTkLabel(
            self.app,
            text="Gestión de Pagos",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        # =========================
        # REGISTRAR PAGO
        # =========================

        lbl_registrar = ctk.CTkLabel(
            self.app,
            text="REGISTRAR PAGO",
            font=("Arial", 18, "bold")
        )
        lbl_registrar.pack(pady=(10, 5))

        self.alumno_id = ctk.CTkEntry(
            self.app,
            placeholder_text="ID Alumno",
            width=300
        )
        self.alumno_id.pack(pady=5)

        self.monto = ctk.CTkEntry(
            self.app,
            placeholder_text="Monto",
            width=300
        )
        self.monto.pack(pady=5)

        self.concepto = ctk.CTkEntry(
            self.app,
            placeholder_text="Concepto",
            width=300
        )
        self.concepto.pack(pady=5)

        boton_guardar = ctk.CTkButton(
            self.app,
            text="Registrar Pago",
            command=self.registrar_pago
        )
        boton_guardar.pack(pady=10)

        # =========================
        # MODIFICAR PAGO
        # =========================

        lbl_modificar = ctk.CTkLabel(
            self.app,
            text="MODIFICAR PAGO",
            font=("Arial", 18, "bold")
        )
        lbl_modificar.pack(pady=(20, 5))

        self.id_modificar = ctk.CTkEntry(
            self.app,
            placeholder_text="ID Pago a modificar",
            width=300
        )
        self.id_modificar.pack(pady=5)

        self.nuevo_monto = ctk.CTkEntry(
            self.app,
            placeholder_text="Nuevo monto",
            width=300
        )
        self.nuevo_monto.pack(pady=5)

        self.nuevo_concepto = ctk.CTkEntry(
            self.app,
            placeholder_text="Nuevo concepto",
            width=300
        )
        self.nuevo_concepto.pack(pady=5)

        boton_modificar = ctk.CTkButton(
            self.app,
            text="Modificar Pago",
            fg_color="orange",
            hover_color="#CC8400",
            command=self.modificar_pago
        )
        boton_modificar.pack(pady=10)

        # =========================
        # COMPROBANTE PDF
        # =========================

        lbl_comprobante = ctk.CTkLabel(
            self.app,
            text="GENERAR COMPROBANTE",
            font=("Arial", 18, "bold")
        )
        lbl_comprobante.pack(pady=(20, 5))

        self.id_comprobante = ctk.CTkEntry(
            self.app,
            placeholder_text="ID Pago para PDF",
            width=300
        )
        self.id_comprobante.pack(pady=5)

        boton_comprobante = ctk.CTkButton(
            self.app,
            text="Generar Comprobante PDF",
            fg_color="green",
            hover_color="darkgreen",
            command=self.generar_comprobante
        )
        boton_comprobante.pack(pady=10)


        boton_vencidos = ctk.CTkButton(
            self.app,
            text="Ver Pagos Vencidos",
            fg_color="darkred",
            hover_color="red",
            command=self.ver_pagos_vencidos
        )
        boton_vencidos.pack(pady=10)


        # =========================
        # BOTÓN VOLVER
        # =========================

        boton_volver = ctk.CTkButton(
            self.app,
            text="Volver",
            fg_color="gray",
            hover_color="darkgray",
            command=self.app.destroy
        )
        boton_volver.pack(pady=10)

        # =========================
        # HISTORIAL
        # =========================

        self.lista_pagos = ctk.CTkTextbox(
            self.app,
            width=650,
            height=300
        )
        self.lista_pagos.pack(pady=20)

        self.cargar_pagos()

    def registrar_pago(self):

        alumno_id = self.alumno_id.get().strip()
        monto = self.monto.get().strip()
        concepto = self.concepto.get().strip()

        if not alumno_id or not monto or not concepto:

            messagebox.showerror(
                "Error",
                "Todos los campos son obligatorios"
            )
            return

        if not alumno_id.isdigit():

            messagebox.showerror(
                "Error",
                "ID Alumno inválido"
            )
            return

        try:
            float(monto)
        except:
            messagebox.showerror(
                "Error",
                "Monto inválido"
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
                "No existe un alumno con ese ID"
            )
            return

        fecha = datetime.now().strftime("%Y-%m-%d")

        fecha_vencimiento = (
            datetime.now() + timedelta(days=30)
        ).strftime("%Y-%m-%d")

        cursor.execute("""
        INSERT INTO pagos
        (alumno_id, monto, fecha, fecha_vencimiento, concepto)
        VALUES (?, ?, ?, ?, ?)
        """, (
            alumno_id,
            monto,
            fecha,
            fecha_vencimiento,
            concepto
        ))


        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Pago registrado correctamente"
        )

        self.alumno_id.delete(0, "end")
        self.monto.delete(0, "end")
        self.concepto.delete(0, "end")

        self.cargar_pagos()

    def modificar_pago(self):

        id_pago = self.id_modificar.get().strip()
        nuevo_monto = self.nuevo_monto.get().strip()
        nuevo_concepto = self.nuevo_concepto.get().strip()

        if not id_pago.isdigit():

            messagebox.showerror(
                "Error",
                "Ingrese un ID de pago válido"
            )
            return

        if not nuevo_monto:

            messagebox.showerror(
                "Error",
                "Ingrese un nuevo monto"
            )
            return

        try:
            float(nuevo_monto)
        except:

            messagebox.showerror(
                "Error",
                "Monto inválido"
            )
            return

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM pagos WHERE id = ?",
            (id_pago,)
        )

        pago = cursor.fetchone()

        if not pago:

            conexion.close()

            messagebox.showerror(
                "Error",
                "No existe un pago con ese ID"
            )
            return

        cursor.execute("""
        UPDATE pagos
        SET monto = ?, concepto = ?
        WHERE id = ?
        """, (
            nuevo_monto,
            nuevo_concepto,
            id_pago
        ))

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Pago actualizado correctamente"
        )

        self.id_modificar.delete(0, "end")
        self.nuevo_monto.delete(0, "end")
        self.nuevo_concepto.delete(0, "end")

        self.cargar_pagos()

    def ver_pagos_vencidos(self):

        self.lista_pagos.delete("1.0", "end")

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
        SELECT
            pagos.id,
            alumnos.nombre,
            alumnos.apellido,
            pagos.monto,
            pagos.fecha_vencimiento
        FROM pagos
        INNER JOIN alumnos
            ON pagos.alumno_id = alumnos.id
        WHERE pagos.fecha_vencimiento < ?
        """, (fecha_actual,))

        vencidos = cursor.fetchall()

        conexion.close()

        self.lista_pagos.insert(
            "end",
            "===== PAGOS VENCIDOS =====\n\n"
        )

        if not vencidos:

            self.lista_pagos.insert(
                "end",
                "No existen pagos vencidos.\n"
            )
            return

        for pago in vencidos:

            self.lista_pagos.insert(
                "end",
                f"Pago ID: {pago[0]}\n"
                f"Alumno: {pago[1]} {pago[2]}\n"
                f"Monto: ${pago[3]}\n"
                f"Fecha Vencimiento: {pago[4]}\n"
                f"{'-'*40}\n"
            )

    def generar_comprobante(self):

        id_pago = self.id_comprobante.get().strip()

        if not id_pago.isdigit():

            messagebox.showerror(
                "Error",
                "Ingrese el ID del pago"
            )
            return

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT
            pagos.id,
            alumnos.nombre,
            alumnos.apellido,
            pagos.monto,
            pagos.fecha,
            pagos.concepto
        FROM pagos
        INNER JOIN alumnos
            ON pagos.alumno_id = alumnos.id
        WHERE pagos.id = ?
        """, (id_pago,))

        pago = cursor.fetchone()

        conexion.close()

        if not pago:

            messagebox.showerror(
                "Error",
                "Pago no encontrado"
            )
            return

        nombre_pdf = f"Comprobante_Pago_{id_pago}.pdf"

        doc = SimpleDocTemplate(nombre_pdf)

        estilos = getSampleStyleSheet()

        contenido = []

        contenido.append(
            Paragraph(
                "SISTEMA DE GESTIÓN MMA",
                estilos["Title"]
            )
        )

        contenido.append(Spacer(1, 20))

        contenido.append(
            Paragraph(
                f"<b>Pago ID:</b> {pago[0]}",
                estilos["Normal"]
            )
        )

        contenido.append(
            Paragraph(
                f"<b>Alumno:</b> {pago[1]} {pago[2]}",
                estilos["Normal"]
            )
        )

        contenido.append(
            Paragraph(
                f"<b>Monto:</b> ${pago[3]}",
                estilos["Normal"]
            )
        )

        contenido.append(
            Paragraph(
                f"<b>Fecha:</b> {pago[4]}",
                estilos["Normal"]
            )
        )

        contenido.append(
            Paragraph(
                f"<b>Concepto:</b> {pago[5]}",
                estilos["Normal"]
            )
        )

        doc.build(contenido)

        self.id_comprobante.delete(0, "end")
        messagebox.showinfo(
            "Éxito",
            f"Comprobante generado:\n{nombre_pdf}"
        )   


    def cargar_pagos(self):

        self.lista_pagos.delete("1.0", "end")

        conexion = sqlite3.connect("mma.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT
            pagos.id,
            alumnos.nombre,
            alumnos.apellido,
            pagos.monto,
            pagos.fecha,
            pagos.fecha_vencimiento,
            pagos.concepto
        FROM pagos
        INNER JOIN alumnos
            ON pagos.alumno_id = alumnos.id
        ORDER BY pagos.id DESC
        """)

        pagos = cursor.fetchall()

        conexion.close()

        self.lista_pagos.insert(
            "end",
            "===== HISTORIAL DE PAGOS =====\n\n"
        )

        if not pagos:

            self.lista_pagos.insert(
                "end",
                "No existen pagos registrados.\n"
            )
            return

        for pago in pagos:

            self.lista_pagos.insert(
                "end",
                f"Pago ID: {pago[0]}\n"
                f"Alumno: {pago[1]} {pago[2]}\n"
                f"Monto: ${pago[3]}\n"
                f"Fecha Pago: {pago[4]}\n"
                f"Fecha Vencimiento: {pago[5]}\n"
                f"Concepto: {pago[6]}\n"
                f"{'-'*50}\n"
            )