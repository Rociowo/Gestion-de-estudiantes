# Main menu

from gestion import add_new_course
from gestion import gestion_cursos
from gestion import gestion_estudiante
from gestion import gestion_universidad

menuVar = 0



















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
            gestion_estudiante.StudentManager()
        elif menuSelection == 2:
            gestion_cursos.ClassroomManager()
        elif menuSelection == 3:
            gestion_universidad.UniversityManager()
        elif menuSelection == 4:
            break
    return menuSelection


Menu()