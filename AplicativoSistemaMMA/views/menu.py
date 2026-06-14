import customtkinter as ctk


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
            text=f"Bienvenido {rol}",
            font=("Arial", 18)
        )
        bienvenida.pack(pady=10)

        self.btn_alumnos = ctk.CTkButton(
            self.app,
            text="Gestión de Alumnos",
            width=250
        )
        self.btn_alumnos.pack(pady=10)

        self.btn_salir = ctk.CTkButton(
            self.app,
            text="Cerrar Sesión",
            width=250,
            fg_color="red",
            hover_color="darkred",
            command=self.app.destroy
        )
        self.btn_salir.pack(pady=10)

    def run(self):
        self.app.mainloop()