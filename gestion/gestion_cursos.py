#Classroom Data Model, Functions and Storage
from gestion import add_new_course
from gestion import gestion_estudiante

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
        
def ShowClassroomData():
    print("\n====== Listado de Cursos Registrados ======")
    add_new_course.courseManager.list_courses()
    
def ClassroomManager():
    print("\n====== Gestion de Cursos ======")
    print("1. Administrar datos de cursos registrados")
    print("2. Listado de cursos registrados")
    print("3. Volver al menu principal")
    try:
        opt1 = int(input("\nSeleccione una opción: "))
        if opt1 == 1:
            try:
                print("\n====== Administrar datos de cursos registrados ======")
                print("1. Registrar nuevo curso")
                print("2. Actualizar curso existente")
                print("3. Asignar estudiante a un curso existente")
                print("4. Desvincular estudiante de un curso existente")
                print("5. Eliminar curso existente")
                print("6. Volver al menu principal")
                optB1 = int(input("\nSeleccione una opción: "))
                if optB1 == 1:
                    codigo = input("Ingrese el codigo del curso: ")
                    nombre = input("Ingrese el nombre del curso: ")
                    descripcion = input("Ingrese la descripcion del curso: ")

                    try:
                        nuevo_curso = add_new_course.courseManager.add_course(
                            codigo, nombre, descripcion
                        )
                        print(f"Curso registrado exitosamente: {nuevo_curso}")
                    except ValueError as e:
                        print(e)

                elif optB1 == 2:
                    ShowClassroomData()
                    codigo = input("Ingrese el código del curso a actualizar: ")
                    nuevo_nombre = input(
                        "Ingrese el nuevo nombre del curso (deje vacío para no cambiar): "
                    )
                    nueva_descripcion = input(
                        "Ingrese la nueva descripción del curso (deje vacío para no cambiar): "
                    )

                    if not nuevo_nombre and not nueva_descripcion:
                        print("No se han proporcionado cambios.")
                    else:
                        actualizado = add_new_course.courseManager.update_course(
                            codigo, nuevo_nombre or None, nueva_descripcion or None
                        )
                        if actualizado:
                            print(
                                f"Curso con código {codigo} actualizado exitosamente."
                            )
                        else:
                            print("No se encontró un curso con ese código.")

                elif optB1 == 3:
                    ShowClassroomData()
                    codigo_curso = input("Ingrese el código del curso: ")

                    try:
                        add_new_course.courseManager.get_course(codigo_curso)
                        gestion_estudiante.ShowStudentData()
                        nro_id = input(
                            "Ingrese el número de Matricula del estudiante: "
                        )

                        asignado = add_new_course.courseManager.add_student_to_course(
                            codigo_curso, nro_id
                        )
                        if asignado:
                            pass
                        else:
                            print("Estudiante no encontrado")
                    except ValueError:
                        print("Curso no encontrado")

                elif optB1 == 4:
                    ShowClassroomData()
                    codigo_curso = input("Ingrese el código del curso: ")

                    curso = add_new_course.courseManager.get_course(codigo_curso)
                    if curso and codigo_curso == curso.codigo:
                        gestion_estudiante.ShowStudentData()
                        nro_id = input(
                            "Ingrese el número de matrícula del estudiante a desvincular: "
                        )
                        desvinculado = (
                            add_new_course.courseManager.remove_student_from_course(
                                codigo_curso, nro_id
                            )
                        )
                        if desvinculado:
                            print(
                                f"Estudiante {nro_id} desvinculado exitosamente del curso {codigo_curso}"
                            )
                        else:
                            print("Estudiante no encontrado o no asignado a este curso")
                    else:
                        print("Curso no encontrado")
                elif optB1 == 5:
                    ShowClassroomData()
                    codigo = input("Ingrese el codigo del curso a eliminar: ")
                    try:
                        deleted_course = add_new_course.courseManager.delete_course(
                            codigo
                        )
                        if deleted_course:
                            print(f"Curso eliminado exitosamente: {codigo}")
                        else:
                            print("Curso no encontrado")
                    except ValueError as e:
                        print(e)
                elif optB1 == 6:
                    pass
                else:
                    print("Opcion Invalida")
            except ValueError:
                print("Opcion Invalida")
        elif opt1 == 2:
            ShowClassroomData()
        elif opt1 == 3:
            pass
        else:
            print("Opcion Invalida")
    except ValueError:
        print("Opcion Invalida")