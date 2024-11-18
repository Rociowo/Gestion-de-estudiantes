# Classroom Data Model, Functions and Storage


class Course:
    def __init__(
        self, codigo: str, nombre: str, descripcion: str = "", estudiantes=None
    ):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.estudiantes = estudiantes or []

    def to_tuple(self):
        return (
            self.codigo,
            self.nombre,
            self.descripcion,
            [estudiante for estudiante in self.estudiantes],
        )
