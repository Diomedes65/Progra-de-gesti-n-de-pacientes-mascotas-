import tkinter as tk
from tkinter import ttk, messagebox

# Base de datos en memoria para almacenamiento temporal
mascotas = {}
historias_clinicas = {}

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Mascotas")
        self.geometry("800x600")
        self.minsize(800, 600)
        
        # Crear el contenedor principal
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (MenuPrincipal, RegistrarMascota, RegistrarHistoria, ConsultarHistoria):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuPrincipal")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MenuPrincipal(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Menú Principal", font=('Helvetica', 18, 'bold'))
        label.pack(pady=20)

        boton_registrar_mascota = ttk.Button(self, text="Registrar Mascota", 
                                            command=lambda: controller.show_frame("RegistrarMascota"))
        boton_registrar_mascota.pack(pady=10)

        boton_registrar_historia = ttk.Button(self, text="Registrar Historia Clínica", 
                                             command=lambda: controller.show_frame("RegistrarHistoria"))
        boton_registrar_historia.pack(pady=10)

        boton_consultar_historia = ttk.Button(self, text="Consultar Historia Clínica", 
                                             command=lambda: controller.show_frame("ConsultarHistoria"))
        boton_consultar_historia.pack(pady=10)

class RegistrarMascota(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Registrar Mascota", font=('Helvetica', 18, 'bold'))
        label.grid(row=0, column=0, columnspan=2, pady=20)

        # Crear formulario
        fields = ["ID", "Tipo de Mascota", "Nombre", "Peso", "Nombre del Dueño", "Teléfono del Dueño", "Dirección", "Detalles de Consulta"]
        self.entries = {}
        for i, field in enumerate(fields):
            label = ttk.Label(self, text=field)
            label.grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(self)
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")
            self.entries[field] = entry

        boton_guardar = ttk.Button(self, text="Guardar", command=self.guardar_mascota)
        boton_guardar.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)

        boton_volver = ttk.Button(self, text="Volver al Menú", 
                                 command=lambda: controller.show_frame("MenuPrincipal"))
        boton_volver.grid(row=len(fields)+2, column=0, columnspan=2, pady=5)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def guardar_mascota(self):
        datos = {field: entry.get() for field, entry in self.entries.items()}
        if datos["ID"] in mascotas:
            messagebox.showerror("Error", "La mascota con esta ID ya está registrada.")
        else:
            mascotas[datos["ID"]] = datos
            messagebox.showinfo("Éxito", "Mascota registrada exitosamente.")

class RegistrarHistoria(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Registrar Historia Clínica", font=('Helvetica', 18, 'bold'))
        label.grid(row=0, column=0, columnspan=2, pady=20)

        self.id_label = ttk.Label(self, text="ID de la Mascota")
        self.id_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.id_entry = ttk.Entry(self)
        self.id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.fields = ["Tipo de Enfermedad", "Observaciones", "Nombre del Veterinario"]
        self.entries = {}
        self.fields_dict = {
            "Tipo de Enfermedad": ["Infección", "Parásitos", "Fractura", "Alergias", "Otro"]
        }

        for i, field in enumerate(self.fields):
            label = ttk.Label(self, text=field)
            label.grid(row=i+2, column=0, padx=10, pady=5, sticky="e")
            if field == "Tipo de Enfermedad":
                entry = ttk.Combobox(self, values=self.fields_dict[field])
            else:
                entry = ttk.Entry(self)
            entry.grid(row=i+2, column=1, padx=10, pady=5, sticky="ew")
            self.entries[field] = entry

        boton_guardar = ttk.Button(self, text="Guardar", command=self.guardar_historia)
        boton_guardar.grid(row=len(self.fields)+2, column=0, columnspan=2, pady=20)

        boton_volver = ttk.Button(self, text="Volver al Menú", 
                                 command=lambda: controller.show_frame("MenuPrincipal"))
        boton_volver.grid(row=len(self.fields)+3, column=0, columnspan=2, pady=5)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def guardar_historia(self):
        id_mascota = self.id_entry.get()
        if id_mascota not in mascotas:
            messagebox.showerror("Error", "No existe una mascota con esta ID.")
        else:
            historia = {field: entry.get() for field, entry in self.entries.items()}
            if id_mascota in historias_clinicas:
                historias_clinicas[id_mascota].append(historia)
            else:
                historias_clinicas[id_mascota] = [historia]
            messagebox.showinfo("Éxito", "Historia clínica registrada exitosamente.")

class ConsultarHistoria(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Consultar Historia Clínica", font=('Helvetica', 18, 'bold'))
        label.grid(row=0, column=0, columnspan=2, pady=20)

        self.id_label = ttk.Label(self, text="ID de la Mascota")
        self.id_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.id_entry = ttk.Entry(self)
        self.id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        boton_consultar = ttk.Button(self, text="Consultar", command=self.consultar_historia)
        boton_consultar.grid(row=2, column=0, columnspan=2, pady=10)

        self.resultado = tk.Text(self, height=10, width=50)
        self.resultado.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        boton_volver = ttk.Button(self, text="Volver al Menú", 
                                 command=lambda: controller.show_frame("MenuPrincipal"))
        boton_volver.grid(row=4, column=0, columnspan=2, pady=5)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def consultar_historia(self):
        id_mascota = self.id_entry.get()
        if id_mascota not in mascotas:
            messagebox.showerror("Error", "No existe una mascota con esta ID.")
        else:
            self.resultado.delete("1.0", tk.END)
            mascota = mascotas[id_mascota]
            self.resultado.insert(tk.END, f"Información de la Mascota:\n")
            for key, value in mascota.items():
                self.resultado.insert(tk.END, f"{key}: {value}\n")
            if id_mascota in historias_clinicas:
                self.resultado.insert(tk.END, f"\nHistorias Clínicas:\n")
                for historia in historias_clinicas[id_mascota]:
                    self.resultado.insert(tk.END, "-----------------------------------\n")
                    for key, value in historia.items():
                        self.resultado.insert(tk.END, f"{key}: {value}\n")
            else:
                self.resultado.insert(tk.END, "\nNo hay historias clínicas registradas.")

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
