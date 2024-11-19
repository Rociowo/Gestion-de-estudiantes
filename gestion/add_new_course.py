from gestion import gestion_estudiante
from gestion.gestion_cursos import Course
import json
import uuid
import os
import datetime

courses_db = []


class courseManager:
    @staticmethod
    def add_course(codigo: str, nombre: str, descripcion: str = "") -> Course:
        if any(course.codigo == codigo for course in courses_db):
            raise ValueError("Ya existe un curso con este código.")

        course = Course(codigo, nombre, descripcion)
        courses_db.append(course)
        return course.to_tuple()

    @staticmethod
    def get_course(codigo: str) -> Course:
        for course in courses_db:
            if course.codigo == codigo:
                return course
        raise None

    @staticmethod
    def update_course(
        codigo: str, nuevo_nombre: str = None, nueva_descripcion: str = None
    ) -> bool:
        for course in courses_db:
            if course.codigo == codigo:
                if nuevo_nombre:
                    course.nombre = nuevo_nombre
                if nueva_descripcion:
                    course.descripcion = nueva_descripcion

            return True
        return False

    def delete_course(codigo: str) -> bool:
        global courses_db
        try:
            curso = next(
                (course for course in courses_db if course.codigo == codigo), None
            )
            if curso:
                if curso.estudiantes:
                    print(
                        f"No se puede eliminar el curso {codigo} porque tiene estudiantes inscritos."
                    )
                    return False

                courses_db = [
                    course for course in courses_db if course.codigo != codigo
                ]

                delete_id = str(uuid.uuid4())
                delete_entry = {
                    "id": delete_id,
                    "codigo": codigo,
                    "accion": "eliminacion",
                    "detalle": f"Curso {codigo} eliminado",
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

                print(f"Curso {codigo} eliminado correctamente.")
                return True
            else:
                print(f"Curso con código {codigo} no encontrado.")
                return False
        except Exception as e:
            print(f"Error al eliminar el curso: {e}")
            return False

    @staticmethod
    def list_courses() -> Course:
        if not courses_db:
            print("No hay cursos registrados.")
            return False
        for course in courses_db:
            print(
                f"Código: {course.codigo}, Nombre: {course.nombre}, Descripción: {course.descripcion}, Estudiantes: {len(course.estudiantes)}"
            )

    @staticmethod
    def add_student_to_course(codigo_curso: str, nro_id: str) -> bool:
        curso = next((c for c in courses_db if c.codigo == codigo_curso), None)
        if not curso:
            print("Curso no encontrado")
            return False

        student = gestion_estudiante.read_student(nro_id)
        if student is None:
            print("Estudiante no encontrado")
            return False

        curso.estudiantes.append(student)

        student.add_course(codigo_curso)

        print(f"Estudiante {nro_id} fue añadido al curso {codigo_curso}")
        return True

    @staticmethod
    def remove_student_from_course(codigo_curso: str, nro_id: str) -> bool:
        curso = next((c for c in courses_db if c.codigo == codigo_curso), None)
        if not curso:
            print("Curso no encontrado")
            return False

        estudiante_a_eliminar = None
        for estudiante in curso.estudiantes:
            if estudiante.identificacion_fija[0] == nro_id:
                estudiante_a_eliminar = estudiante
                break

        if not estudiante_a_eliminar:
            print("Estudiante no encontrado en este curso")
            return False

        curso.estudiantes.remove(estudiante_a_eliminar)

        estudiante_a_eliminar.remove_course(codigo_curso)

        print(
            f"Estudiante con matrícula {nro_id} ha sido eliminado del curso {codigo_curso}"
        )
        return True