# Student Data Model and Functions

from typing import Dict, Optional
import os
import ast
import re
import json
import uuid
import datetime


def validar_rut(rut: str) -> bool:
    try:
        if not isinstance(rut, str):
            raise ValueError("El RUT debe ser una cadena de texto.")

        rut = rut.strip().upper()

        if not re.match(r"^\d{7,8}-[0-9Kk]{1}$", rut):
            raise ValueError(
                "Formato de RUT inválido. Debe ser XXXXXXXX-X o XXXXXXX-X."
            )

        rut_sin_dv, dv = rut.split("-")

        if not rut_sin_dv.isdigit():
            raise ValueError("La parte numérica del RUT debe contener solo dígitos.")

        if len(rut_sin_dv) < 7 or len(rut_sin_dv) > 8:
            raise ValueError("El número de dígitos antes del guion debe ser 7 u 8.")

        suma = 0
        multiplicador = 2
        for i in range(len(rut_sin_dv) - 1, -1, -1):
            suma += int(rut_sin_dv[i]) * multiplicador
            multiplicador = 9 if multiplicador == 2 else multiplicador + 1

        dv_calculado = 11 - (suma % 11)
        if dv_calculado == 11:
            dv_calculado = "0"
        elif dv_calculado == 10:
            dv_calculado = "K"
        else:
            dv_calculado = str(dv_calculado)

        if dv_calculado.lower() != dv.lower():
            raise ValueError(
                f"Dígito verificador incorrecto. Se esperaba {dv_calculado}."
            )

        return True
    except ValueError as e:
        print(f"Error de validación: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False


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
            save_grades()

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
                promedios[curso] = round(sum(notas) / len(notas), 1)
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
    filepath = "gestion/datos_estudiantes.py"

    try:
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
                    fixed_data = [
                        student for student in fixed_data if student[0] != nro_id
                    ]
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

        if delete:
            delete_id = str(uuid.uuid4())
            delete_entry = {
                "id": delete_id,
                "nro_id": nro_id,
                "accion": "eliminacion",
                "detalle": f"Estudiante con ID {nro_id} eliminado de datos fijos",
                "fecha": str(datetime.datetime.now()),
            }

            dir_path = "gestion/db_sys/"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            file_path = os.path.join(dir_path, "registro_eliminaciones.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    registros = json.load(f)
            else:
                registros = []

            registros.append(delete_entry)

            with open(file_path, "w") as f:
                json.dump(registros, f, indent=4)

    except Exception as e:
        print(f"Error al guardar o eliminar datos fijos del estudiante {nro_id}: {e}")


def get_fixed_data():
    filepath = "gestion/datos_estudiantes.py"
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
    if not validar_rut(rut):
        raise ValueError("RUT inválido. No se puede crear el estudiante.")

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
    try:
        student = students_db.pop(nro_id, None)
        if student:
            save_fixed_data(
                nro_id,
                student.identificacion_fija[1],
                student.identificacion_fija[2],
                delete=True,
            )
            delete_grades(nro_id)
            save_grades()

            delete_id = str(uuid.uuid4())
            delete_entry = {
                "id": delete_id,
                "nro_id": nro_id,
                "accion": "eliminacion",
                "detalle": f"Estudiante con ID {nro_id} eliminado",
                "fecha": str(datetime.datetime.now()),
            }

            dir_path = "gestion/db_sys/"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            file_path = os.path.join(dir_path, "registro_eliminaciones.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    registros = json.load(f)
            else:
                registros = []

            registros.append(delete_entry)

            with open(file_path, "w") as f:
                json.dump(registros, f, indent=4)

            print(f"Estudiante con ID {nro_id} eliminado correctamente.")
            return True
        else:
            print(f"Estudiante con ID {nro_id} no encontrado.")
            return False
    except Exception as e:
        print(f"Error al eliminar estudiante: {e}")
        return False


def delete_grades(nro_id: str):
    try:
        filepath = os.path.join("gestion", "calificaciones.py")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                lines = f.readlines()

            grades_data = []
            for line in lines[1:-1]:
                grade_entry = ast.literal_eval(line.strip().strip(","))
                if grade_entry["nro_id"] != nro_id:
                    grades_data.append(grade_entry)

            with open(filepath, "w") as f:
                f.write("calificaciones = [\n")
                for data in grades_data:
                    f.write(f"    {data},\n")
                f.write("]\n")
        else:
            print(f"El archivo {filepath} no existe.")
    except Exception as e:
        print(
            f"Error al eliminar las calificaciones del estudiante con ID {nro_id}: {e}"
        )


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
    filepath = "gestion/calificaciones.py"

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
