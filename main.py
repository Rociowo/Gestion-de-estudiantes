# Main menu

import os
import json
from gestion.add_new_course import courses_db
from datetime import datetime
from gestion.gestion_cursos import Course
from gestion.gestion_estudiante import Student, students_db
from gestion import add_new_course
from gestion import gestion_estudiante
from gestion import gestion_universidad
from gestion.gestion_universidad import SedeManager
from gestion.gestion_universidad import SedeUniversitaria
import uuid

try:
    from gestion.calificaciones import calificaciones
except ImportError:
    calificaciones = []

try:
    from gestion.datos_estudiantes import datos_fijos_estudiantes
except ImportError:
    datos_fijos_estudiantes = []

try:
    from gestion.datos_universidad import sedes_registradas
except ImportError:
    sedes_registradas = []


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
    
    while True:
        print("\n====== Gestion de Estudiantes ======")
        print("1. Administrar datos de estudiantes")
        print("2. Listado de estudiantes registrados")
        print("3. Volver al menu principal")
        try:
            opt2 = int(input("\nSeleccione una opción: "))
            if opt2 == 1:
                while True:
                    
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
                
                ShowStudentData()
            elif opt2 == 3:
                break
            else:
                print("Opcion Invalida")
        except ValueError:
            print("Opcion Invalida")


def UniversityManager():
    
    while True:
        print("\n====== Gestion de Sedes Universitarias ======")
        print("1. Administrar datos de sedes registradas")
        print("2. Listado de sedes registradas")
        print("3. Volver al menú principal")
        try:
            opt3 = int(input("\nSeleccione una opción: "))
            if opt3 == 1:
                while True:
                    
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
            "fecha": str(datetime.now()),
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
                with open(file_path, "r", encoding="utf-8") as f:
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
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(registros, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"Error al escribir en el archivo {file_path}: {e}")
        except Exception as e:
            print(f"Error inesperado al escribir en el archivo {file_path}: {e}")

    except Exception as e:
        print(f"Error inesperado general al vaciar los archivos: {e}")


def agregar_timestamps(datos):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"timestamp": timestamp, "data": datos}


def guardar_datos_json():
    try:
        ruta_json = "gestion/db_sys/datos_registrados.json"
        os.makedirs(os.path.dirname(ruta_json), exist_ok=True)

        calificaciones = cargar_archivo_python(
            "gestion/calificaciones.py", "calificaciones"
        )
        datos_fijos_estudiantes = cargar_archivo_python(
            "gestion/datos_estudiantes.py", "datos_fijos_estudiantes"
        )
        sedes_registradas = cargar_archivo_python(
            "gestion/datos_universidad.py", "sedes_registradas"
        )

        students_db_data = {
            key: {key_attr: value for key_attr, value in vars(student).items()}
            if isinstance(student, Student)
            else student
            for key, student in students_db.items()
        }

        courses_db_data = [
            {key: value for key, value in vars(course).items()}
            if isinstance(course, Course)
            else course
            for course in courses_db
        ]

        datos = {
            "courses_db": courses_db_data,
            "calificaciones_db": calificaciones,
            "estudiantes_db": datos_fijos_estudiantes,
            "universidades_db": sedes_registradas,
            "students_db": students_db_data,
        }

        with open(ruta_json, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

        print(f"Datos guardados exitosamente en '{ruta_json}'.")

    except FileNotFoundError as e:
        print(f"Error al guardar los datos: archivo no encontrado - {e}")
    except PermissionError as e:
        print(f"Error de permisos al intentar guardar los datos en {ruta_json}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error en el formato JSON al guardar los datos: {e}")
    except OSError as e:
        print(f"Error del sistema operativo al intentar acceder al archivo: {e}")
    except IOError as e:
        print(f"Error de entrada/salida al guardar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado al guardar los datos en JSON: {e}")


def cargar_archivo_python(filepath, var_name):
    try:
        if not os.path.exists(filepath) or os.stat(filepath).st_size == 0:
            print(
                f"El archivo {filepath} no existe o está vacío. Se creará una variable vacía."
            )
            return []
        with open(filepath, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        local_vars = {}
        exec(contenido, {}, local_vars)
        return local_vars.get(var_name, [])
    except Exception as e:
        print(f"Error al cargar el archivo {filepath}: {e}")
        return []


def guardar_archivo_python(filepath, var_name, data):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as archivo:
            archivo.write(f"{var_name} = {repr(data)}")
        print(f"Archivo '{filepath}' guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el archivo {filepath}: {e}")


def cargar_datos_json():
    try:
        ruta_json = "gestion/db_sys/datos_registrados.json"
        if not os.path.exists(ruta_json):
            print(f"El archivo '{ruta_json}' no existe. No se cargaron datos.")
            return

        with open(ruta_json, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        global \
            calificaciones, \
            datos_fijos_estudiantes, \
            sedes_registradas, \
            students_db, \
            courses_db

        calificaciones = datos.get("calificaciones_db", [])
        datos_fijos_estudiantes = [
            (item[0], item[1], item[2]) for item in datos.get("estudiantes_db", [])
        ]
        sedes_registradas = datos.get("universidades_db", [])
        courses_db = datos.get("courses_db", [])

        if "students_db" in datos and isinstance(datos["students_db"], dict):
            students_db = {}
            for key, value in datos["students_db"].items():
                identificacion_fija = value.get("identificacion_fija", [])
                if len(identificacion_fija) >= 3:
                    nro_id, rut, nombre_completo = identificacion_fija[:3]
                else:
                    nro_id = rut = nombre_completo = None
                student_data = {
                    k: v
                    for k, v in value.items()
                    if k not in ["identificacion_fija", "notas", "cursos"]
                }
                if nro_id and rut and nombre_completo:
                    students_db[key] = Student(
                        nro_id=nro_id,
                        rut=rut,
                        nombre_completo=nombre_completo,
                        **student_data,
                    )
                else:
                    print(
                        f"Faltan datos necesarios para crear el estudiante con ID {key}"
                    )
        else:
            students_db = {}

        if "courses_db" in datos:
            courses_db = datos["courses_db"]

        guardar_archivo_python(
            "gestion/calificaciones.py", "calificaciones", calificaciones
        )
        guardar_archivo_python(
            "gestion/datos_estudiantes.py",
            "datos_fijos_estudiantes",
            datos_fijos_estudiantes,
        )
        guardar_archivo_python(
            "gestion/datos_universidad.py", "sedes_registradas", sedes_registradas
        )

        print("Datos cargados exitosamente desde JSON y archivos .py actualizados.")

    except json.JSONDecodeError as e:
        print(f"Error en el formato del archivo JSON '{ruta_json}': {e}")
    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
    except KeyError as e:
        print(f"Clave no encontrada en el JSON: {e}")
    except Exception as e:
        print(f"Error al cargar los datos desde JSON: {e}")


if __name__ == "__main__":
    while True:
        print("\n" + "=" * 40)
        print(" Sistema de Gestión - Manejo de Datos ")
        print("=" * 40)
        print("1. Respaldar datos en JSON")
        print("2. Cargar datos desde JSON")
        print("3. Ingresar al sistema")
        try:
            opcion = int(input("\nSeleccione una opción: "))
            if opcion == 1:
                guardar_datos_json()
            elif opcion == 2:
                cargar_datos_json()
            elif opcion == 3:
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida.")
        except ValueError:
            print("Debe ingresar un número válido.")


def Menu():
    
    cargar_datos_json()
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
            guardar_datos_json()
            vaciar_archivos()
            break


Menu()
