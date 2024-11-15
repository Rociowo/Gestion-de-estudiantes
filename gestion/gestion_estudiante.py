# Student Data Model and Functions

from typing import Dict, Optional
import os
import ast


class Student:
    def __init__(self, nro_id: str, rut: str, nombre_completo: str):
        self.identificacion_fija = (nro_id, rut, nombre_completo)
        self.cursos = []
        self.notas = {}

    def add_course(self, curso):
        if curso not in self.cursos:
            self.cursos.append(curso)
            self.notas[curso] = []

    def remove_course(self, curso):
        if curso in self.cursos:
            self.cursos.remove(curso)
            del self.notas[curso]

    def add_grade(self, curso: str, nota: float):
        if curso in self.cursos:
            if 1.0 <= nota <= 7.0:
                self.notas[curso].append(nota)
            else:
                raise ValueError("La nota debe estar entre 1.0 y 7.0")
        else:
            raise ValueError(f"El curso: '{curso}' no está registrado")

    def get_grades(self, codigo_curso):
        if codigo_curso in self.notas:
            return self.notas.get(codigo_curso)
        return []

    def update_grades(self, codigo_curso, nuevas_calificaciones):
        if codigo_curso in self.notas:
            self.notas[codigo_curso] = nuevas_calificaciones

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


def save_fixed_data(nro_id: str, rut: str, nombre_completo: str, delete: bool = False):
    filepath = "Management/datos_estudiantes.py"

    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()

        if len(lines) > 1:
            fixed_data = []
            for line in lines[1:-1]:
                cleaned_line = line.strip().strip("',")
                student = ast.literal_eval(cleaned_line)
                fixed_data.append(student)

            if delete:
                fixed_data = [student for student in fixed_data if student[0] != nro_id]
            else:
                fixed_data.append((nro_id, rut, nombre_completo))
        else:
            fixed_data = [(nro_id, rut, nombre_completo)]

    else:
        fixed_data = [(nro_id, rut, nombre_completo)]

    with open(filepath, "w") as f:
        f.write("datos_fijos_estudiantes = [\n")
        for student in fixed_data:
            f.write(f"    ('{student[0]}', '{student[1]}', '{student[2]}'),\n")
        f.write("]\n")


def get_fixed_data():
    filepath = "Management/datos_estudiantes.py"
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        lines = f.readlines()
        if (len(lines)) > 1:
            return [tuple(line.strip()[2:-2].split("', '")) for line in lines[1:-1]]
        else:
            return []


def create_student(nro_id: str, rut: str, nombre_completo: str) -> Student:
    if nro_id in students_db:
        raise ValueError("El estudiante con este número de ID ya existe.")
    for student in students_db.values():
        if student.identificacion_fija[1] == rut:
            raise ValueError("El estudiante con este número de rut ya existe.")

    fixed_data = get_fixed_data()
    if any(student[0] == nro_id for student in fixed_data):
        raise ValueError("El estudiante con este número de ID ya existe.")
    if any(student[1] == rut for student in fixed_data):
        raise ValueError("El estudiante con este número de rut ya existe.")
    student = Student(nro_id, rut, nombre_completo)
    students_db[nro_id] = student
    save_fixed_data(nro_id, rut, nombre_completo)
    return student


def read_student(nro_id: str) -> Optional[Student]:
    student = students_db.get(nro_id)
    if student:
        return student
    return None


def update_student(nro_id: str, nuevo_nombre_completo: Optional[str] = None) -> bool:
    student = students_db.get(nro_id)
    if not student:
        print("Estudiante no encontrado")
        return False

    rut = student.identificacion_fija[1]
    nombre_completo = student.identificacion_fija[2]

    if nuevo_nombre_completo:
        nombre_completo = nuevo_nombre_completo

    delete_student(nro_id)
    create_student(nro_id, rut, nombre_completo)
    print("Estudiante actualizado con éxito")


def delete_student(nro_id: str) -> bool:
    student = students_db.pop(nro_id, None)
    if student:
        save_fixed_data(
            nro_id,
            student.identificacion_fija[1],
            student.identificacion_fija[2],
            delete=True,
        )
        return True
    return False


def list_students() -> Dict[str, Dict]:
    if not students_db:
        print("No hay estudiantes registrados")
        return

    sorted_students = sorted(students_db.items(), key=lambda x: x[0])
    for nro_id, student in sorted_students:
        print(f"ID: {nro_id}")
        print(f"Nombre Completo: {student.identificacion_fija[2]}")
        print(f"Rut: {student.identificacion_fija[1]}")
        print(
            f"Cursos: {','.join(student.cursos) if student.cursos else 'Estudiante sin cursos inscritos'}"
        )
        print(f"Promedio: {student.calculate_average()}")
        print("=" * 30)


def save_grades():
    filepath = "Management/calificaciones.py"

    grades_data = []
    for nro_id, student in students_db.items():
        student_grades = {
            "nro_id": nro_id,
            "nombre_completo": student.identificacion_fija[2],
            "notas": student.notas,
        }
        grades_data.append(student_grades)

    with open(filepath, "w") as f:
        f.write("calificaciones = [\n")
        for data in grades_data:
            f.write(f"    {data},\n")
        f.write("]\n")
    print(f"Calificaciones guardadas exitosamente en {filepath}")