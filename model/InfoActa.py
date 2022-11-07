"""
Contiene la clase InfoActa e
internamente tiene sus respectivos atributos.
Asignatura: POO
"""


class InfoActa:

    # Constructor
    def __init__(self, criterios) -> None:
        super().__init__()

        # Datos del acta
        self.autor = ""
        self.fecha_acta = ""
        self.fecha_presentacion = "" #punto3
        self.nombre_trabajo = ""
        self.tipo_trabajo = ""
        self.director = ""
        self.codirector = " "
        self.jurado1 = ""
        self.jurado1Escoger = False
        self.jurado2 = ""
        self.jurado2Escoger = False
        self.nota_final = 0.0
        self.criterios = criterios
        self.estado = False
        self.cantidadProyectos = 0 #punto 10
        self.cantidadInvestigaciones = 0 #punto 10
        self.cantidadJuradosExternos = 0
        self.cantidadJuradosInternos = 0
        self.cantidadNotaSuperior = 0

