# Student Data Model and Functions

from typing import Dict, Optional


class Student:
    def __init__(self, nro_id: str, rut: str, nombre_completo: str):
        self.identificacion_fija = (nro_id, nombre_completo)
        self.rut = rut
        self.cursos = []
        self.notas = {}

    def add_course(self, curso):
        if curso not in self.cursos:
            self.cursos.append(curso)
            self.notas[curso] = []

    def add_grade(self, curso: str, nota: float):
        if curso in self.cursos:
            if 1.0 <= nota <= 7.0:
                self.notas[curso].append(nota)
            else:
                raise ValueError("La nota debe estar entre 1.0 y 7.0")
        else:
            raise ValueError(f"El curso: '{curso}' no está registrado")

    def calculate_average(self) -> Dict[str, float]:
        promedios = {}
        for curso, notas in self.notas.items():
            if notas:
                promedios[curso] = sum(notas) / len(notas)
            else:
                promedios[curso] = 0.0
        return promedios

    def to_dict(self) -> Dict:
        return {
            "nro_id": self.identificacion_fija[0],
            "nombre_completo": self.identificacion_fija[1],
            "rut": self.rut,
            "cursos": self.cursos,
            "notas": self.notas,
        }


students_db: Dict[str, Student] = {}


def create_student(nro_id: str, rut: str, nombre_completo: str) -> Student:
    if nro_id in students_db:
        raise ValueError("El estudiante con este número de ID ya existe.")
    for student in students_db.values():
        if student.rut == rut:
            raise ValueError("El estudiante con este número de rut ya existe.")
    for student in students_db.values():
        if student.identificacion_fija[1] == student.identificacion_fija[1]:
            raise ValueError("El estudiante con este nombre ya existe.")
    student = Student(nro_id, rut, nombre_completo)
    students_db[nro_id] = student
    return student


def read_student(nro_id: str) -> Optional[Student]:
    return students_db.get(nro_id)


def update_student(nro_id: str, nombre_completo: Optional[str] = None) -> bool:
    student = students_db.get(nro_id)
    if not student:
        return False
    if nombre_completo:
        student.identificacion_fija = (student.identificacion_fija[0], nombre_completo)
    return True


def delete_student(nro_id: str) -> bool:
    student = students_db.pop(nro_id, None)
    if student:
        return True
    return False


def list_students() -> Dict[str, Dict]:
    if not students_db:
        print("No hay estudiantes reegistrados")
        return

    sorted_students = sorted(students_db.items(), key=lambda x: x[0])
    for nro_id, student in sorted_students:
        print(f"ID: {nro_id}")
        print(f"Nombre Completo: {student.identificacion_fija[1]}")
        print(f"Rut: {student.rut}")
        print(
            f"Cursos: {','.join(student.cursos) if student.cursos else 'Estudiante sin cursos inscritos'}"
        )
        print(f"Promedio: {student.calculate_average()}")
        print("=" * 30)