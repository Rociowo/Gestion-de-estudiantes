# Main menu
seleccionMenu = 0

#from gestion import Calificaciones
#from gestion import datos_estudiante
#from gestion import datos_universidad
#from gestion import gestion_cursos
from gestion import gestion_estudiante
#from gestion import gestion_universidad
#from gestion import add_new_course



def mostrarDataDeEstudiantes():
    print("\n====== Listado de estudiantes registrados ======")
    gestion_estudiante.list_students()
    
def mostrarDataDeCursos():
    pass   

def mostrarDataDeUniversidades():
    pass

def dataDeEstudiantes():
    pass

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
                print("3. Eliminar curso existente")
                optB1 = int(input("\nSeleccione una opción: "))
                if optB1 == 1:
                    pass
                elif optB1 == 2:
                    pass
                elif optB1 == 3:
                    pass
                else:
                    print("Opcion Invalida")
            except ValueError:
                print("Opcion Invalida")
        elif opt1 == 2:
            mostrarDataDeCursos()
        elif opt1 == 3:
            pass
        else:
            print("Opcion Invalida")
    except ValueError:
        print("Opcion Invalida")

def gestionDeEstudiante():
    print("\n====== Gestion de estudiantes ======")
    print("1. Administrar datos de estudiantes")
    print("2. Listado de estudiantes registrados")
    print("3. Volver al menu principal")
    try:
        opt = int(input("\nSeleccione una opcion: "))
        if opt == 1:
            try:
                print("\n====== Administrar datos de estudiantes ======")
                print("1. Registrar nuevo estudiante")
                print("2. Actualizar estudiante existente")
                print("3. Eliminar estudiante existente")
                optB = int(input("\nSeleccione una opcion: "))
                if optB == 1:
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
                            f" Estudiante {new_student.identificacion_fija[1]} registrado con exito"
                        )
                    except Exception as e:
                        print(e)
                elif optB == 2:
                    pass
                elif optB == 3:
                    mostrarDataDeEstudiantes()
                    nro_id = str(
                        input(
                            "Ingrese el número de matricula del estudiante a eliminar: "
                        )
                    )
                    gestion_estudiante.delete_student(nro_id)
                else:
                    print("Opcion Invalida")
            except ValueError:
                print("Opcion Invalida")
        elif opt == 2:
            mostrarDataDeEstudiantes()
        elif opt == 3:
            pass
        else:
            print("Opcion invalida")
    except ValueError:
        print("Opcion invalida")

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
            mostrarDataDeUniversidades()
        elif opt3 == 3:
            pass
        else:
            print("Opcion Invalida")
    except ValueError:
        print("Opcion Invalida")





def Menu ():
    seleccionMenu = 0
    while seleccionMenu < 1 or seleccionMenu > 3:
        print("\n=====Software de gestion de estudiantes=====")
        print("""
        1. Gestion de estudiantes
        2. Gestion de cursos
        3. Gestion de universidad
        4. Salir""")
        seleccionMenu = int(input("Seleccione una opcion: "))
        if seleccionMenu < 1 or seleccionMenu > 7:      
            print("Opcion invalida")
            return seleccionMenu
        if seleccionMenu == 1:
            gestionDeEstudiante()
        elif seleccionMenu == 2:
            pass
        elif seleccionMenu == 3:
            pass
        elif seleccionMenu == 4:
            break
    return seleccionMenu

while seleccionMenu != 4:   
    seleccionMenu = Menu()
    if seleccionMenu == 4:
        break