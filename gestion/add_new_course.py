from gestion import gestion_estudiante
from gestion.gestion_cursos import Course

courses_db = []


class courseManager:
    @staticmethod
    def add_course(codigo: str, nombre: str, descripcion: str = "") -> Course:
        if any(course[0] == codigo for course in courses_db):
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

    @staticmethod
    def delete_course(codigo: str) -> bool:
        global courses_db
        courses_db = [course for course in courses_db if course[0] != codigo]
        return True

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