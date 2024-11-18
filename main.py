# Main menu

from gestion import add_new_course
from gestion import gestion_estudiante
from gestion import gestion_universidad
from gestion.gestion_universidad import SedeManager
from gestion.gestion_universidad import SedeUniversitaria
import os
import json
import uuid
import datetime

menuVar = 0


def ShowClassroomData():
    print("\n====== Listado de Cursos Registrados ======")
    add_new_course.courseManager.list_courses()


def ShowStudentData():
    print("\n====== Listado de Estudiantes Registrados ======")
    gestion_estudiante.list_students()


def ShowUniversityData():
    sede_manager = SedeManager()
    sede_manager.list_sedes()


def verificar_estudiante_existente(nro_id):
    estudiante = gestion_estudiante.read_student(nro_id)
    if estudiante:
        print(f"El estudiante con número de matrícula {nro_id} ya está registrado.")
        return True
    return False


def ClassroomManager():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n" + "=" * 40)
        print(f"{' Sistema de Gestión de Cursos ':^40}")
        print("=" * 40)
        print(""" 
        1.  Gestionar datos de cursos
        2.  Listado de cursos registrados
        3.  Volver al menu principal
        """)

        try:
            opt1 = int(input("\nSeleccione una opción: "))
            if opt1 == 1:
                while True:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("\n" + "=" * 40)
                    print(f"{' Gestion de datos de cursos ':^40}")
                    print("=" * 40)
                    print(""" 
                    1. Registrar nuevo curso
                    2. Administrar cursos existentes
                    3. Eliminar cursos existentes
                    4. Volver al menu principal
                    """)

                    try:
                        optB1 = int(input("\nSeleccione una opción: "))
                        if optB1 == 1:
                            os.system("cls" if os.name == "nt" else "clear")
                            print("\n" + "=" * 40)
                            print(f"{' Registrar Nuevo Curso ':^40}")
                            print("=" * 40)
                            codigo = input("Ingrese el código del curso: ")
                            nombre = input("Ingrese el nombre del curso: ")
                            descripcion = input("Ingrese la descripción del curso: ")

                            try:
                                nuevo_curso = add_new_course.courseManager.add_course(
                                    codigo, nombre, descripcion
                                )
                                print(f"Curso registrado exitosamente: {nuevo_curso}")
                            except ValueError as e:
                                print(f"Error: {e}")
                        elif optB1 == 2:
                            os.system("cls" if os.name == "nt" else "clear")
                            print("\n" + "=" * 40)
                            print(f"{' Administrar Cursos ':^40}")
                            print("=" * 40)
                            ShowClassroomData()
                            codigo_curso = input(
                                "Ingrese el código del curso a administrar: "
                            )
                            curso = add_new_course.courseManager.get_course(
                                codigo_curso
                            )
                            if not curso:
                                print("Curso no encontrado.")
                            else:
                                print(
                                    f"\n{'Opciones para el curso: ' + curso.nombre + ' - ' + curso.codigo:^40}"
                                )
                                print(""" 
                                1. Actualizar datos del curso
                                2. Asignar estudiante
                                3. Desvincular estudiante
                                4. Agregar notas a un estudiante
                                5. Eliminar notas a un estudiante
                                6. Volver
                                """)
                                try:
                                    optCurso = int(input("\nSeleccione una opción: "))
                                    if optCurso == 1:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print("\n" + "=" * 40)
                                        print(f"{' Actualizar Curso ':^40}")
                                        print("=" * 40)
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
                                                codigo_curso,
                                                nuevo_nombre or None,
                                                nueva_descripcion or None,
                                            )
                                            if actualizado:
                                                print(
                                                    f"Curso con código {codigo_curso} actualizado exitosamente."
                                                )
                                            else:
                                                print(
                                                    "No se encontró un curso con ese código."
                                                )
                                    elif optCurso == 2:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print("\n" + "=" * 40)
                                        print(f"{' Asignar Estudiante ':^40}")
                                        print("=" * 40)
                                        ShowStudentData()
                                        nro_id = input(
                                            "Ingrese el número de Matrícula del estudiante: "
                                        )
                                        asignado = add_new_course.courseManager.add_student_to_course(
                                            codigo_curso, nro_id
                                        )
                                        if asignado:
                                            print(
                                                f"Estudiante {nro_id} asignado al curso {codigo_curso} exitosamente."
                                            )
                                        else:
                                            print("Estudiante no encontrado")
                                    elif optCurso == 3:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print("\n" + "=" * 40)
                                        print(f"{' Desvincular Estudiante ':^40}")
                                        print("=" * 40)
                                        ShowStudentData()
                                        nro_id = input(
                                            "Ingrese el número de matrícula del estudiante a desvincular: "
                                        )
                                        desvinculado = add_new_course.courseManager.remove_student_from_course(
                                            codigo_curso, nro_id
                                        )
                                        if desvinculado:
                                            print(
                                                f"Estudiante {nro_id} desvinculado exitosamente del curso {codigo_curso}"
                                            )
                                        else:
                                            print(
                                                "Estudiante no encontrado o no asignado a este curso"
                                            )
                                    elif optCurso == 4:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print("\n" + "=" * 40)
                                        print(f"{' Agregar Notas ':^40}")
                                        print("=" * 40)
                                        ShowStudentData()
                                        nro_id = input(
                                            "Ingrese el número de Matricula del estudiante: "
                                        )
                                        estudiante = gestion_estudiante.read_student(
                                            nro_id
                                        )
                                        if not estudiante:
                                            print("Estudiante no encontrado")
                                        elif codigo_curso not in estudiante.cursos:
                                            print(
                                                f"El estudiante {nro_id} no está inscrito en el curso {codigo_curso}."
                                            )
                                        else:
                                            try:
                                                nota = float(
                                                    input(
                                                        "Ingrese la nota (1.0 a 7.0): "
                                                    )
                                                )
                                                estudiante.add_grade(codigo_curso, nota)
                                                gestion_estudiante.save_grades()
                                                print(
                                                    f"Nota {nota} añadida al estudiante {nro_id} en el curso {codigo_curso}."
                                                )
                                            except ValueError as ve:
                                                print(f"Error: {ve}")
                                            except Exception:
                                                print(
                                                    "Ocurrió un error al registrar la nota"
                                                )
                                    elif optCurso == 5:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print("\n" + "=" * 40)
                                        print(f"{' Eliminar Notas ':^40}")
                                        print("=" * 40)
                                        ShowStudentData()
                                        nro_id = input(
                                            "Ingrese el número de Matrícula del estudiante: "
                                        )
                                        estudiante = gestion_estudiante.read_student(
                                            nro_id
                                        )

                                        if not estudiante:
                                            print("Estudiante no encontrado.")
                                        elif codigo_curso not in estudiante.cursos:
                                            print(
                                                f"El estudiante {nro_id} no está inscrito en el curso {codigo_curso}."
                                            )
                                        else:
                                            try:
                                                notas_curso = estudiante.get_grades(
                                                    codigo_curso
                                                )
                                                if not isinstance(notas_curso, list):
                                                    print(
                                                        "Error: las calificaciones no están disponibles como una lista."
                                                    )
                                                elif (
                                                    not notas_curso
                                                    or len(notas_curso) == 0
                                                ):
                                                    print(
                                                        f"El estudiante {nro_id} no tiene calificaciones en el curso {codigo_curso}."
                                                    )
                                                else:
                                                    print(
                                                        "\nCalificaciones actuales en el curso:"
                                                    )
                                                    for idx, nota in enumerate(
                                                        notas_curso, 1
                                                    ):
                                                        print(f"{idx}. {nota}")
                                                    indice = int(
                                                        input(
                                                            "Seleccione el número de la calificación a eliminar: "
                                                        )
                                                    )
                                                    if 1 <= indice <= len(notas_curso):
                                                        nota_eliminada = (
                                                            notas_curso.pop(indice - 1)
                                                        )
                                                        estudiante.update_grades(
                                                            codigo_curso, notas_curso
                                                        )
                                                        gestion_estudiante.save_grades()
                                                        print(
                                                            f"Calificación {nota_eliminada} eliminada exitosamente."
                                                        )
                                                    else:
                                                        print("Índice inválido.")
                                            except ValueError as ve:
                                                print(f"Error: {ve}")
                                            except Exception as e:
                                                print(f"Ocurrió un error: {e}")
                                    elif optCurso == 6:
                                        break
                                    else:
                                        print("Opción Invalida")
                                except ValueError:
                                    print("Error al procesar la solicitud")

                        elif optB1 == 3:
                            os.system("cls" if os.name == "nt" else "clear")
                            print("\n" + "=" * 40)
                            print(f"{' Eliminar Curso ':^40}")
                            print("=" * 40)
                            ShowClassroomData()
                            codigo = input("Ingrese el código del curso a eliminar: ")
                            try:
                                deleted_course = (
                                    add_new_course.courseManager.delete_course(codigo)
                                )
                                if deleted_course:
                                    print(f"Curso eliminado exitosamente: {codigo}")
                                else:
                                    pass
                            except ValueError as e:
                                print(f"Error: {e}")
                        elif optB1 == 4:
                            break
                        else:
                            print("Opción Inválida")
                    except ValueError:
                        print("Error: Entrada no válida")

            elif opt1 == 2:
                os.system("cls" if os.name == "nt" else "clear")
                print("\n" + "=" * 40)
                print(f"{' Listado de Cursos ':^40}")
                print("=" * 40)
                ShowClassroomData()
                input("\nPresione Enter para volver al menú.")
            elif opt1 == 3:
                break
            else:
                print("Opción Invalida")
        except ValueError:
            print("Opción Inválida")


def StudentManager():
    os.system("cls" if os.name == "nt" else "clear")
    while True:
        print("\n====== Gestion de Estudiantes ======")
        print("1. Administrar datos de estudiantes")
        print("2. Listado de estudiantes registrados")
        print("3. Volver al menu principal")
        try:
            opt2 = int(input("\nSeleccione una opción: "))
            if opt2 == 1:
                while True:
                    os.system("cls" if os.name == "nt" else "clear")
                    print(
                        "\n====== Administrar datos de estudiantes registrados ======"
                    )
                    print("1. Registrar nuevo estudiante")
                    print("2. Actualizar estudiante existente")
                    print("3. Eliminar estudiante existente")
                    print("4. Volver al menu principal")
                    try:
                        optB2 = int(input("\nSeleccione una opción: "))
                        if optB2 == 1:
                            nro_id = input(
                                "Ingrese el número de matricula del estudiante: "
                            )
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
                                gestion_estudiante.update_student(
                                    nro_id, nuevo_nombre_completo
                                )
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
                            break
                        else:
                            print("Opcion Invalida")
                    except ValueError:
                        print("Opcion Invalida")
            elif opt2 == 2:
                os.system("cls" if os.name == "nt" else "clear")
                ShowStudentData()
            elif opt2 == 3:
                break
            else:
                print("Opcion Invalida")
        except ValueError:
            print("Opcion Invalida")


def UniversityManager():
    os.system("cls" if os.name == "nt" else "clear")
    while True:
        print("\n====== Gestion de Sedes Universitarias ======")
        print("1. Administrar datos de sedes registradas")
        print("2. Listado de sedes registradas")
        print("3. Volver al menú principal")
        try:
            opt3 = int(input("\nSeleccione una opción: "))
            if opt3 == 1:
                while True:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("\n====== Administrar datos de sedes registradas ======")
                    print("1. Registrar nueva sede")
                    print("2. Actualizar sede existente")
                    print("3. Eliminar sede existente")
                    print("4. Volver al menú principal")
                    try:
                        optB3 = int(input("\nSeleccione una opción: "))
                        if optB3 == 1:
                            try:
                                id_sede = input(
                                    "Ingrese el ID de la nueva sede: "
                                ).strip()
                                sede_manager = SedeManager()
                                sedes_registradas = sede_manager.get_all_sedes()

                                if sedes_registradas is None or not isinstance(
                                    sedes_registradas, list
                                ):
                                    sedes_registradas = []

                                if any(
                                    sede.id_sede == id_sede
                                    for sede in sedes_registradas
                                ):
                                    print(f"Ya existe una sede con ID {id_sede}")
                                    return

                                nombre = input(
                                    "Ingrese el nombre de la nueva sede: "
                                ).strip()
                                direccion = input(
                                    "Ingrese la dirección de la nueva sede: "
                                ).strip()
                                telefono = gestion_universidad.pedir_numero_telefono()

                                nueva_sede = SedeUniversitaria(
                                    id_sede, nombre, direccion, telefono
                                )
                                sede_manager.add_sede(nueva_sede)

                            except ValueError as ve:
                                print(f"Error: {ve}")
                            except Exception as e:
                                print(f"Error al registrar la nueva sede: {e}")

                        elif optB3 == 2:
                            ShowUniversityData()
                            id_sede = input(
                                "Ingrese el ID de la sede a actualizar: "
                            ).strip()
                            sede_manager = SedeManager()
                            sede = sede_manager.get_sede_by_id(id_sede)

                            if not sede:
                                print(f"Sede con ID {id_sede} no encontrada.")
                            else:
                                nombre = input(
                                    "Ingrese el nuevo nombre (dejar en blanco para no cambiar): "
                                ).strip()
                                direccion = input(
                                    "Ingrese la nueva dirección (dejar en blanco para no cambiar): "
                                ).strip()
                                telefono = (
                                    gestion_universidad.pedir_numero_telefono()
                                    if input(
                                        "¿Desea actualizar el número de teléfono? (s/n): "
                                    )
                                    .strip()
                                    .lower()
                                    == "s"
                                    else None
                                )

                                sede_manager.update_sede(
                                    id_sede,
                                    nombre=nombre if nombre else None,
                                    direccion=direccion if direccion else None,
                                    telefono=telefono if telefono else None,
                                )
                                print(
                                    f"Sede con ID {id_sede} actualizada exitosamente."
                                )
                        elif optB3 == 3:
                            ShowUniversityData()
                            id_sede = input(
                                "Ingrese el ID de la sede a eliminar: "
                            ).strip()
                            sede_manager = SedeManager()
                            sede = sede_manager.get_sede_by_id(id_sede)

                            if not sede:
                                print(f"Sede con ID {id_sede} no encontrada.")
                            else:
                                sede_manager.delete_sede(id_sede)
                                print(f"Sede con ID {id_sede} eliminada exitosamente.")
                        elif optB3 == 4:
                            break
                        else:
                            print("Opción inválida.")
                    except ValueError:
                        print("Opción inválida.")

            elif opt3 == 2:
                os.system("cls" if os.name == "nt" else "clear")
                ShowUniversityData()
            elif opt3 == 3:
                print("Volviendo al menú principal...")
                break
            else:
                print("Opción inválida.")
        except ValueError:
            print("Opción inválida.")


def obtener_opcion_valida(min_val, max_val):
    while True:
        try:
            seleccion = int(input("\nSeleccione una opción: "))
            if min_val <= seleccion <= max_val:
                return seleccion
            else:
                print(f"✘ Opción inválida. Debe estar entre {min_val} y {max_val}.")
        except ValueError:
            print("✘ Error: Por favor ingrese un número válido.")


def vaciar_archivos():
    try:
        archivos = [
            "gestion/datos_estudiantes.py",
            "gestion/datos_universidad.py",
            "gestion/calificaciones.py",
        ]

        for archivo in archivos:
            try:
                with open(archivo, "w"):
                    pass
            except PermissionError as e:
                print(f"Error de permisos al vaciar el archivo {archivo}: {e}")
            except FileNotFoundError as e:
                print(f"Archivo no encontrado {archivo}: {e}")
            except OSError as e:
                print(
                    f"Error relacionado con el sistema de archivos al vaciar {archivo}: {e}"
                )
            except Exception as e:
                print(f"Error inesperado al vaciar el archivo {archivo}: {e}")

        print("Contenido de los archivos eliminado exitosamente.")

        delete_id = str(uuid.uuid4())
        delete_entry = {
            "id": delete_id,
            "accion": "vaciar_archivos",
            "detalle": "Contenido de los archivos datos_estudiantes.py, datos_universidad.py y calificaciones.py eliminado.",
            "archivos_afectados": archivos,
            "fecha": str(datetime.datetime.now()),
        }

        dir_path = "gestion/db_sys/"
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except OSError as e:
                print(f"Error al crear directorio {dir_path}: {e}")
                return
            except Exception as e:
                print(f"Error inesperado al crear directorio {dir_path}: {e}")
                return

        file_path = os.path.join(dir_path, "registro_eliminaciones_archivos.json")

        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    try:
                        registros = json.load(f)
                    except json.JSONDecodeError as e:
                        print(f"Error al leer el archivo JSON {file_path}: {e}")
                        registros = []
            else:
                registros = []
        except OSError as e:
            print(f"Error al acceder al archivo {file_path}: {e}")
            registros = []

        registros.append(delete_entry)

        try:
            with open(file_path, "w") as f:
                json.dump(registros, f, indent=4)
        except OSError as e:
            print(f"Error al escribir en el archivo {file_path}: {e}")
        except Exception as e:
            print(f"Error inesperado al escribir en el archivo {file_path}: {e}")

    except Exception as e:
        print(f"Error inesperado general al vaciar los archivos: {e}")


def Menu():
    os.system("cls" if os.name == "nt" else "clear")
    while True:
        print("\n" + "=" * 40)
        print(" Sistema de Gestión de Estudiantes ")
        print("=" * 40)
        print(""" 
        1.  Gestión de Estudiantes
        2.  Gestión de Cursos
        3.  Gestión de Universidades
        4.  Cerrar
        """)

        menuSelection = obtener_opcion_valida(1, 4)

        if menuSelection == 1:
            try:
                print("\n🔹 Accediendo a la Gestión de Estudiantes...")
                StudentManager()
            except Exception as e:
                print(f"✘ Error en la gestión de estudiantes: {e}")
        elif menuSelection == 2:
            try:
                print("\n🔹 Accediendo a la Gestión de Cursos...")
                ClassroomManager()
            except Exception as e:
                print(f"✘ Error en la gestión de cursos: {e}")
        elif menuSelection == 3:
            try:
                print("\n🔹 Accediendo a la Gestión de Universidades...")
                UniversityManager()
            except Exception as e:
                print(f"✘ Error en la gestión de universidades: {e}")
        elif menuSelection == 4:
            print("\n💻 Cerrando el sistema...")
            vaciar_archivos()
            break


Menu()
