#Classroom Data Model, Functions and Storage

class Course:
    def init(self, codigo: str, nombre: str, descripcion: str = ""):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.estudiantes = []

    def to_tuple(self):
        return (
            self.codigo,
            self.nombre,
            self.descripcion,
            [estudiante for estudiante in self.estudiantes],
        )