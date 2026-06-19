import customtkinter as ctk
from views.alumnos import AlumnosWindow
from views.entrenadores import EntrenadoresWindow
from views.pagos import PagosWindow
from views.asistencia import AsistenciaWindow

class MenuWindow:

    def __init__(self, rol):

        self.app = ctk.CTk()

        self.app.title("Sistema MMA")
        self.app.geometry("700x500")

        self.rol = rol

        titulo = ctk.CTkLabel(
            self.app,
            text="Sistema de Gestión MMA",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        bienvenida = ctk.CTkLabel(
            self.app,
            text=f"Bienvenido al Sistema MMA\nRol: {rol}",
            font=("Arial", 18)
        )
        bienvenida.pack(pady=10)

        # ADMINISTRADOR
        if rol == "Administrador":

            self.btn_alumnos = ctk.CTkButton(
                self.app,
                text="Gestión de Alumnos",
                width=250,
                command=self.abrir_alumnos
            )
            self.btn_alumnos.pack(pady=10)

            self.btn_entrenadores = ctk.CTkButton(
                self.app,
                text="Gestión de Entrenadores",
                width=250,
                command=self.abrir_entrenadores
            )
            self.btn_entrenadores.pack(pady=10)

            self.btn_pagos = ctk.CTkButton(
                self.app,
                text="Gestión de Pagos",
                width=250,
                command=self.abrir_pagos
            )
            self.btn_pagos.pack(pady=10)

        # RECEPCIONISTA
        elif rol == "Recepcionista":

            self.btn_alumnos = ctk.CTkButton(
                self.app,
                text="Gestión de Alumnos",
                width=250,
                command=self.abrir_alumnos
            )
            self.btn_alumnos.pack(pady=10)

            self.btn_entrenadores = ctk.CTkButton(
                self.app,
                text="Gestión de Entrenadores",
                width=250,
                command=self.abrir_entrenadores
            )
            self.btn_entrenadores.pack(pady=10)

            self.btn_pagos = ctk.CTkButton(
                self.app,
                text="Gestión de Pagos",
                width=250,
                command=self.abrir_pagos
            )
            self.btn_pagos.pack(pady=10)

        # ENTRENADOR
        elif rol == "Entrenador":

            lbl_info = ctk.CTkLabel(
                self.app,
                text="Acceso de Entrenador\nConsulta de alumnos",
                font=("Arial", 16)
            )
            lbl_info.pack(pady=10)

        self.btn_asistencia = ctk.CTkButton(
            self.app,
            text="Control de Asistencia",
            width=250,
            command=self.abrir_asistencia
        )
        self.btn_asistencia.pack(pady=10)

        self.btn_salir = ctk.CTkButton(
            self.app,
            text="Cerrar Sesión",
            width=250,
            fg_color="red",
            hover_color="darkred",
            command=self.app.destroy
        )
        self.btn_salir.pack(pady=10)



    def abrir_alumnos(self):

        AlumnosWindow()

    def abrir_entrenadores(self):

        EntrenadoresWindow()
    
    def abrir_pagos(self):

        PagosWindow()


    def abrir_asistencia(self):

        ventana = AsistenciaWindow()

    def run(self):

        self.app.mainloop()