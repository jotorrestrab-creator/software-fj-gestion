"""Interfaz gráfica de escritorio para Software FJ usando Tkinter.

Ejecutar desde la carpeta raíz con: python -X utf8 interfaz.py
"""
import tkinter as tk
from tkinter import ttk, messagebox

from clientes import Cliente, GestorClientes
from servicios import CatalogoServicios, ServicioSala, ServicioEquipo, ServicioAsesoria
from reservas import GestorReservas
from excepciones import ErrorSistemaFJ
from logger_config import LOGGER


class AplicacionSoftwareFJ:
    """Interfaz gráfica conectada con las clases de negocio existentes."""

    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ | Gestión integral")
        self.root.geometry("1120x720")
        self.root.minsize(900, 600)

        self.gestor_clientes = GestorClientes()
        self.catalogo = CatalogoServicios()
        self.gestor_reservas = GestorReservas()

        self._estilos()
        self._construir()
        self._cargar_servicios_demo()
        self._actualizar()

    def _estilos(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Titulo.TLabel", font=("Segoe UI", 22, "bold"),
                        foreground="#172B4D", background="#F3F6FB")
        style.configure("Subtitulo.TLabel", font=("Segoe UI", 10),
                        foreground="#667085", background="#F3F6FB")
        style.configure("Seccion.TLabel", font=("Segoe UI", 12, "bold"),
                        foreground="#172B4D", background="#FFFFFF")
        style.configure("Tarjeta.TFrame", background="#FFFFFF", relief="flat")
        style.configure("TarjetaTitulo.TLabel", font=("Segoe UI", 9),
                        foreground="#667085", background="#FFFFFF")
        style.configure("TarjetaValor.TLabel", font=("Segoe UI", 19, "bold"),
                        foreground="#172B4D", background="#FFFFFF")
        style.configure("Treeview", rowheight=32, font=("Segoe UI", 9),
                        background="#FFFFFF", fieldbackground="#FFFFFF",
                        foreground="#344054", borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                        background="#EAF0F6", foreground="#344054", padding=9)
        style.map("Treeview", background=[("selected", "#DCEBFA")],
                  foreground=[("selected", "#172B4D")])
        style.configure("TLabel", font=("Segoe UI", 9))
        style.configure("TEntry", padding=7)
        style.configure("TCombobox", padding=6)
        style.configure("Accion.TButton", padding=(10, 8),
                        font=("Segoe UI", 9, "bold"))
        style.configure("TButton", padding=(9, 7))
        style.configure("TLabelframe", background="#FFFFFF")
        style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"),
                        foreground="#172B4D", background="#FFFFFF")
        style.configure("TNotebook", background="#F3F6FB", borderwidth=0)
        style.layout("Oculto.TNotebook.Tab", [])

    def _construir(self):
        self.root.configure(bg="#F3F6FB")
        contenedor = tk.Frame(self.root, bg="#F3F6FB")
        contenedor.pack(fill="both", expand=True)

        # Menú lateral de navegación.
        lateral = tk.Frame(contenedor, bg="#172B4D", width=205)
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)
        tk.Label(lateral, text="SOFTWARE FJ", bg="#172B4D", fg="#FFFFFF",
                 font=("Segoe UI", 17, "bold")).pack(anchor="w", padx=20, pady=(28, 2))
        tk.Label(lateral, text="GESTIÓN INTEGRAL", bg="#172B4D", fg="#AFC2DA",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=21, pady=(0, 30))
        self.nav_botones = []
        for texto, indice in (("▦  Clientes", 0), ("▤  Servicios", 1), ("▣  Reservas", 2)):
            boton = tk.Button(
                lateral, text=texto, anchor="w", relief="flat", bd=0,
                bg="#172B4D", fg="#DCE6F2", activebackground="#29466D",
                activeforeground="#FFFFFF", font=("Segoe UI", 10),
                padx=20, pady=13, cursor="hand2",
                command=lambda i=indice: self._mostrar_tab(i)
            )
            boton.pack(fill="x", padx=10, pady=3)
            self.nav_botones.append(boton)
        tk.Label(lateral, text="SOFTWARE FJ  •  v1.0", bg="#172B4D",
                 fg="#8FA5C0", font=("Segoe UI", 8)).pack(side="bottom", pady=18)

        # Área principal.
        principal = tk.Frame(contenedor, bg="#F3F6FB")
        principal.pack(side="left", fill="both", expand=True)
        encabezado = tk.Frame(principal, bg="#F3F6FB")
        encabezado.pack(fill="x", padx=26, pady=(22, 13))
        ttk.Label(encabezado, text="Panel de gestión", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(encabezado,
                  text="Administra clientes, servicios y reservas desde un solo lugar.",
                  style="Subtitulo.TLabel").pack(anchor="w", pady=(3, 0))

        # Indicadores rápidos.
        indicadores = tk.Frame(principal, bg="#F3F6FB")
        indicadores.pack(fill="x", padx=26, pady=(0, 15))
        self.valor_clientes = tk.StringVar(value="0")
        self.valor_servicios = tk.StringVar(value="0")
        self.valor_reservas = tk.StringVar(value="0")
        self.valor_confirmadas = tk.StringVar(value="0")
        for titulo, variable in (
            ("CLIENTES REGISTRADOS", self.valor_clientes),
            ("SERVICIOS DISPONIBLES", self.valor_servicios),
            ("RESERVAS CREADAS", self.valor_reservas),
            ("RESERVAS CONFIRMADAS", self.valor_confirmadas),
        ):
            tarjeta = ttk.Frame(indicadores, style="Tarjeta.TFrame", padding=(15, 12))
            tarjeta.pack(side="left", fill="both", expand=True, padx=(0, 10))
            ttk.Label(tarjeta, text=titulo, style="TarjetaTitulo.TLabel").pack(anchor="w")
            ttk.Label(tarjeta, textvariable=variable, style="TarjetaValor.TLabel").pack(anchor="w", pady=(5, 0))

        self.estado = tk.StringVar(value="Sistema listo.")
        barra_estado = tk.Frame(principal, bg="#E7EDF5")
        barra_estado.pack(side="bottom", fill="x", padx=26, pady=(10, 18))
        tk.Label(barra_estado, textvariable=self.estado, bg="#E7EDF5",
                 fg="#475467", font=("Segoe UI", 9), anchor="w",
                 padx=12, pady=9).pack(fill="x")

        self.tabs = ttk.Notebook(principal, style="Oculto.TNotebook")
        self.tabs.pack(fill="both", expand=True, padx=26, pady=(0, 4))
        self.tab_clientes = ttk.Frame(self.tabs, padding=14)
        self.tab_servicios = ttk.Frame(self.tabs, padding=14)
        self.tab_reservas = ttk.Frame(self.tabs, padding=14)
        self.tabs.add(self.tab_clientes, text="Clientes")
        self.tabs.add(self.tab_servicios, text="Servicios")
        self.tabs.add(self.tab_reservas, text="Reservas")

        self._tab_clientes()
        self._tab_servicios()
        self._tab_reservas()
        self._mostrar_tab(0)

    def _mostrar_tab(self, indice):
        self.tabs.select(indice)
        for posicion, boton in enumerate(self.nav_botones):
            if posicion == indice:
                boton.configure(bg="#29466D", fg="#FFFFFF")
            else:
                boton.configure(bg="#172B4D", fg="#DCE6F2")
        titulos = ("Módulo de clientes", "Catálogo de servicios", "Gestión de reservas")
        self.estado.set(titulos[indice])

    def _campo(self, parent, label, variable):
        ttk.Label(parent, text=label).pack(anchor="w", pady=(7, 0))
        ttk.Entry(parent, textvariable=variable, width=31).pack(fill="x", pady=(3, 2))

    def _tabla(self, parent, columns, headings, widths):
        frame = ttk.Frame(parent)
        frame.pack(side="right", fill="both", expand=True, padx=(18, 0))
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, heading, width in zip(columns, headings, widths):
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="w")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tree

    def _tab_clientes(self):
        form = ttk.LabelFrame(self.tab_clientes, text="Registrar cliente", padding=14)
        form.pack(side="left", fill="y")
        self.nombre = tk.StringVar()
        self.correo = tk.StringVar()
        self.telefono = tk.StringVar()
        self._campo(form, "Nombre completo", self.nombre)
        self._campo(form, "Correo electrónico", self.correo)
        self._campo(form, "Teléfono", self.telefono)
        ttk.Button(form, text="Registrar cliente", style="Accion.TButton",
                   command=self._registrar_cliente).pack(fill="x", pady=(12, 5))
        ttk.Button(form, text="Limpiar", command=self._limpiar_cliente).pack(fill="x")
        self.tabla_clientes = self._tabla(
            self.tab_clientes, ("nombre", "correo", "telefono"),
            ("Nombre", "Correo", "Teléfono"), (170, 210, 120)
        )

    def _tab_servicios(self):
        form = ttk.LabelFrame(self.tab_servicios, text="Agregar servicio", padding=14)
        form.pack(side="left", fill="y")
        self.tipo = tk.StringVar(value="Sala")
        self.nombre_servicio = tk.StringVar()
        self.tarifa = tk.StringVar()
        self.extra = tk.StringVar()
        ttk.Label(form, text="Tipo de servicio").pack(anchor="w")
        tipo = ttk.Combobox(
            form, textvariable=self.tipo,
            values=("Sala", "Alquiler de equipo", "Asesoría"),
            state="readonly", width=27
        )
        tipo.pack(fill="x", pady=(3, 8))
        tipo.bind("<<ComboboxSelected>>", self._etiqueta_extra)
        self._campo(form, "Nombre del servicio", self.nombre_servicio)
        self._campo(form, "Tarifa base ($)", self.tarifa)
        self.extra_label = ttk.Label(form, text="Capacidad de la sala (personas)")
        self.extra_label.pack(anchor="w", pady=(7, 0))
        ttk.Entry(form, textvariable=self.extra, width=30).pack(fill="x", pady=(3, 8))
        ttk.Button(form, text="Agregar servicio", style="Accion.TButton",
                   command=self._agregar_servicio).pack(fill="x", pady=(10, 5))
        ttk.Button(form, text="Limpiar", command=self._limpiar_servicio).pack(fill="x")
        self.tabla_servicios = self._tabla(
            self.tab_servicios,
            ("tipo", "nombre", "tarifa", "detalle", "disponible"),
            ("Tipo", "Servicio", "Tarifa base", "Capacidad / detalle", "Disponible"),
            (125, 155, 105, 190, 90)
        )

    def _tab_reservas(self):
        form = ttk.LabelFrame(self.tab_reservas, text="Crear y administrar reservas", padding=14)
        form.pack(side="left", fill="y")
        self.cliente_sel = tk.StringVar()
        self.servicio_sel = tk.StringVar()
        self.duracion = tk.StringVar(value="1")
        ttk.Label(form, text="Cliente").pack(anchor="w")
        self.combo_clientes = ttk.Combobox(
            form, textvariable=self.cliente_sel, state="readonly", width=31
        )
        self.combo_clientes.pack(fill="x", pady=(3, 10))
        ttk.Label(form, text="Servicio").pack(anchor="w")
        self.combo_servicios = ttk.Combobox(
            form, textvariable=self.servicio_sel, state="readonly", width=31
        )
        self.combo_servicios.pack(fill="x", pady=(3, 10))
        self._campo(form, "Duración / cantidad", self.duracion)
        ttk.Button(form, text="Crear reserva", style="Accion.TButton",
                   command=self._crear_reserva).pack(fill="x", pady=(12, 7))
        ttk.Separator(form).pack(fill="x", pady=8)
        ttk.Label(form, text="Selecciona una reserva en la tabla:").pack(anchor="w")
        ttk.Button(form, text="Confirmar", command=self._confirmar).pack(fill="x", pady=(7, 4))
        ttk.Button(form, text="Procesar", command=self._procesar).pack(fill="x", pady=4)
        ttk.Button(form, text="Cancelar", command=self._cancelar).pack(fill="x", pady=4)
        self.tabla_reservas = self._tabla(
            self.tab_reservas,
            ("id", "cliente", "servicio", "cantidad", "estado", "total"),
            ("ID", "Cliente", "Servicio", "Cantidad", "Estado", "Total"),
            (85, 145, 145, 75, 100, 110)
        )

    def _cargar_servicios_demo(self):
        for servicio in (
            ServicioSala("Sala Norte", 75000, 10),
            ServicioEquipo("Proyector", 35000, 4),
            ServicioAsesoria("Asesoría Python", 95000, "Programación orientada a objetos"),
        ):
            self.catalogo.agregar(servicio)

    def _etiqueta_extra(self, _event=None):
        textos = {
            "Sala": "Capacidad de la sala (personas)",
            "Alquiler de equipo": "Unidades disponibles",
            "Asesoría": "Especialidad",
        }
        self.extra_label.configure(text=textos[self.tipo.get()])

    def _registrar_cliente(self):
        try:
            cliente = Cliente(self.nombre.get(), self.correo.get(), self.telefono.get())
            self.gestor_clientes.registrar(cliente)
            self._actualizar()
            self._limpiar_cliente()
            self._estado("Cliente registrado correctamente.")
        except (ErrorSistemaFJ, ValueError) as exc:
            messagebox.showerror("Error al registrar cliente", str(exc), parent=self.root)

    def _agregar_servicio(self):
        try:
            tipo, nombre, tarifa, extra = (
                self.tipo.get(), self.nombre_servicio.get(),
                self.tarifa.get(), self.extra.get()
            )
            if tipo == "Sala":
                servicio = ServicioSala(nombre, tarifa, int(extra))
            elif tipo == "Alquiler de equipo":
                servicio = ServicioEquipo(nombre, tarifa, int(extra))
            else:
                servicio = ServicioAsesoria(nombre, tarifa, extra)
            self.catalogo.agregar(servicio)
            self._actualizar()
            self._limpiar_servicio()
            self._estado("Servicio agregado correctamente.")
        except (ErrorSistemaFJ, ValueError) as exc:
            messagebox.showerror("Error al agregar servicio", str(exc), parent=self.root)

    def _crear_reserva(self):
        try:
            ci, si = self.combo_clientes.current(), self.combo_servicios.current()
            if ci < 0 or si < 0:
                raise ValueError("Selecciona un cliente y un servicio.")
            cliente = self.gestor_clientes.clientes[ci]
            servicio = self.catalogo.servicios[si]
            reserva = self.gestor_reservas.crear(cliente, servicio, self.duracion.get())
            self._actualizar()
            self._seleccionar_id(reserva.id)
            messagebox.showinfo(
                "Reserva creada",
                f"Reserva: {reserva.id[:8]}\nTotal: $ {reserva.total}\nEstado: {reserva.estado.value}",
                parent=self.root
            )
            self._estado("Reserva creada en estado Pendiente.")
        except (ErrorSistemaFJ, ValueError) as exc:
            messagebox.showerror("Error al crear reserva", str(exc), parent=self.root)

    def _reserva_seleccionada(self):
        seleccion = self.tabla_reservas.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona una reserva", "Elige una reserva de la tabla.", parent=self.root)
            return None
        rid = self.tabla_reservas.item(seleccion[0], "values")[0]
        return next((r for r in self.gestor_reservas.reservas if r.id == rid), None)

    def _confirmar(self):
        try:
            reserva = self._reserva_seleccionada()
            if reserva:
                reserva.confirmar()
                self._actualizar()
                self._seleccionar_id(reserva.id)
                self._estado("Reserva confirmada.")
        except ErrorSistemaFJ as exc:
            messagebox.showerror("No se pudo confirmar", str(exc), parent=self.root)

    def _procesar(self):
        try:
            reserva = self._reserva_seleccionada()
            if reserva:
                total = reserva.procesar()
                messagebox.showinfo("Procesamiento exitoso", f"Total calculado: $ {total}", parent=self.root)
                self._estado(f"Reserva procesada. Total: $ {total}")
        except ErrorSistemaFJ as exc:
            messagebox.showerror("No se pudo procesar", str(exc), parent=self.root)

    def _cancelar(self):
        try:
            reserva = self._reserva_seleccionada()
            if reserva and messagebox.askyesno(
                "Confirmar cancelación",
                f"¿Deseas cancelar la reserva {reserva.id[:8]}?",
                parent=self.root
            ):
                reserva.cancelar("Cancelada desde la interfaz")
                self._actualizar()
                self._seleccionar_id(reserva.id)
                self._estado("Reserva cancelada.")
        except ErrorSistemaFJ as exc:
            messagebox.showerror("No se pudo cancelar", str(exc), parent=self.root)

    def _actualizar(self):
        for tree in (self.tabla_clientes, self.tabla_servicios, self.tabla_reservas):
            tree.delete(*tree.get_children())

        for c in self.gestor_clientes.clientes:
            self.tabla_clientes.insert("", "end", values=(c.nombre, c.correo, c.telefono))

        for s in self.catalogo.servicios:
            tipo = type(s).__name__.replace("Servicio", "")
            detalle = getattr(s, "capacidad", getattr(
                s, "unidades_disponibles", getattr(s, "especialidad", "—")
            ))
            self.tabla_servicios.insert(
                "", "end",
                values=(tipo, s.nombre, f"$ {s.tarifa_base}", detalle,
                        "Sí" if s.disponible else "No")
            )

        for r in self.gestor_reservas.reservas:
            self.tabla_reservas.insert(
                "", "end",
                values=(r.id, r.cliente.nombre, r.servicio.nombre,
                        str(r.duracion_horas), r.estado.value, f"$ {r.total}")
            )

        self.combo_clientes["values"] = [
            f"{c.nombre} — {c.correo}" for c in self.gestor_clientes.clientes
        ]
        self.combo_servicios["values"] = [
            f"{s.nombre} — $ {s.tarifa_base}" for s in self.catalogo.servicios
        ]
        self.valor_clientes.set(str(len(self.gestor_clientes.clientes)))
        self.valor_servicios.set(str(sum(1 for s in self.catalogo.servicios if s.disponible)))
        self.valor_reservas.set(str(len(self.gestor_reservas.reservas)))
        self.valor_confirmadas.set(str(sum(
            1 for r in self.gestor_reservas.reservas
            if r.estado.value == "Confirmada"
        )))

    def _seleccionar_id(self, rid):
        for item in self.tabla_reservas.get_children():
            if self.tabla_reservas.item(item, "values")[0] == rid:
                self.tabla_reservas.selection_set(item)
                self.tabla_reservas.focus(item)
                break

    def _limpiar_cliente(self):
        self.nombre.set("")
        self.correo.set("")
        self.telefono.set("")

    def _limpiar_servicio(self):
        self.nombre_servicio.set("")
        self.tarifa.set("")
        self.extra.set("")

    def _estado(self, texto):
        self.estado.set(texto)
        LOGGER.info("Interfaz: %s", texto)


def iniciar():
    root = tk.Tk()
    AplicacionSoftwareFJ(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar()
