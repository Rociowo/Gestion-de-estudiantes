# Main menu

from gestion import add_new_course

# from Management import calificaciones
# from Management import datos_estudiantes
# from Management import datos_universidad
from gestion import gestion_estudiante
# from Management import gestion_universidad

menuVar = 0


def ShowClassroomData():
    print("\n====== Listado de Cursos Registrados ======")
    add_new_course.courseManager.list_courses()


def ShowStudentData():
    print("\n====== Listado de Estudiantes Registrados ======")
    gestion_estudiante.list_students()


def ShowUniversityData():
    print("\n====== Listado de Sedes Registradas ======")
    # TODO: University Database


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
                        ShowStudentData()
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
                        ShowStudentData()
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


def StudentManager():
    print("\n====== Gestion de Estudiantes ======")
    print("1. Administrar datos de estudiantes")
    print("2. Listado de estudiantes registrados")
    print("3. Volver al menu principal")
    try:
        opt2 = int(input("\nSeleccione una opción: "))
        if opt2 == 1:
            try:
                print("\n====== Administrar datos de estudiantes registrados ======")
                print("1. Registrar nuevo estudiante")
                print("2. Actualizar estudiante existente")
                print("3. Eliminar estudiante existente")
                print("4. Volver al menu principal")
                optB2 = int(input("\nSeleccione una opción: "))
                if optB2 == 1:
                    nro_id = input("Ingrese el número de matricula del estudiante: ")
                    rut = input("Ingrese el RUT del estudiante: ")
                    nombre_completo = input(
                        "Ingrese el nombre completo del estudiante: "
                    )

                    try:
                        new_student = gestion_estudiante.create_student(
                            nro_id, rut, nombre_completo
                        )
                        print(
                            f" Estudiante {new_student.identificacion_fija[2]} registrado con exito"
                        )
                    except Exception as e:
                        print(e)
                elif optB2 == 2:
                    ShowStudentData()
                    nro_id = str(
                        input(
                            "Ingrese el número de matricula del estudiante a actualizar: "
                        )
                    )
                    retrieved_student = gestion_estudiante.read_student(nro_id)
                    if retrieved_student is None:
                        print("Estudiante no encontrado")
                    else:
                        nuevo_nombre_completo = str(
                            input("Ingrese el nombre del estudiante: ")
                        )
                        gestion_estudiante.update_student(nro_id, nuevo_nombre_completo)

                elif optB2 == 3:
                    ShowStudentData()
                    nro_id = str(
                        input(
                            "Ingrese el número de matricula del estudiante a eliminar: "
                        )
                    )
                    gestion_estudiante.delete_student(nro_id)
                    print("Estuidante Eliminado")
                elif optB2 == 4:
                    pass
                else:
                    print("Opcion Invalida")
            except ValueError:
                print("Opcion Invalida")
        elif opt2 == 2:
            ShowStudentData()
        elif opt2 == 3:
            pass
        else:
            print("Opcion Invalida")
    except ValueError:
        print("Opcion Invalida")


def UniversityManager():
    print("\n====== Gestion de Sedes Universitarias ======")
    print("1. Administrar datos de sedes registradas")
    print("2. Listado de sedes registradas")
    print("3. Volver al menu principal")
    try:
        opt3 = int(input("\nSeleccione una opción: "))
        if opt3 == 1:
            try:
                print("\n====== Administrar datos de sedes registrados ======")
                print("1. Registrar nueva sede")
                print("2. Actualizar sede existente")
                print("3. Eliminar sede existente")
                optB3 = int(input("\nSeleccione una opción: "))
                if optB3 == 1:
                    pass
                elif optB3 == 2:
                    pass
                elif optB3 == 3:
                    pass
                else:
                    print("Opcion Invalida")
            except ValueError:
                print("Opcion Invalida")
        elif opt3 == 2:
            ShowUniversityData()
        elif opt3 == 3:
            pass
        else:
            print("Opcion Invalida")
    except ValueError:
        print("Opcion Invalida")


def Menu():
    menuSelection = 0
    while menuVar < 1 or menuVar > 4:
        print("\n====== Sistema de Gestion de Estudiantes ======")
        print("""
        1.Gestion de Estudiantes
        2.Gestion de Cursos
        3.Gestion de Universidades
        4.Cerrar""")
        menuSelection = int(input("\nSeleccione una opcion: "))
        if menuSelection < 1 or menuSelection > 7:
            print("Opcion Invalida")
            return menuSelection
        if menuSelection == 1:
            StudentManager()
        elif menuSelection == 2:
            ClassroomManager()
        elif menuSelection == 3:
            UniversityManager()
        elif menuSelection == 4:
            break
    return menuSelection


Menu()