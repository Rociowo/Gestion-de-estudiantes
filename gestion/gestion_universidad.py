def ShowUniversityData():
    print("\n====== Listado de Sedes Registradas ======")
    # TODO: University Database
    
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
