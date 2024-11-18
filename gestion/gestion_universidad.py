import os
import subprocess
import sys
import json
import uuid
import datetime

try:
    import phonenumbers
    from phonenumbers import (
        parse,
        is_valid_number,
        format_number,
        PhoneNumberFormat,
    )

    print("El módulo phonenumbers ya está instalado.")
except ImportError:
    print("El módulo phonenumbers no está instalado, instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "phonenumbers"])
    import phonenumbers
    from phonenumbers import (
        parse,
        is_valid_number,
        format_number,
        PhoneNumberFormat,
    )

    print("El módulo phonenumbers ha sido instalado correctamente.")


class SedeUniversitaria:
    def __init__(self, id_sede, nombre, direccion, telefono):
        self.id_sede = id_sede
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

    def to_dict(self):
        return {
            "id_sede": self.id_sede,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "telefono": self.telefono,
        }

    @staticmethod
    def from_dict(data):
        return SedeUniversitaria(
            id_sede=data["id_sede"],
            nombre=data["nombre"],
            direccion=data["direccion"],
            telefono=data["telefono"],
        )

    @staticmethod
    def format_telefono(telefono, pais):
        try:
            numero = parse(telefono, pais)
            if is_valid_number(numero):
                return format_number(numero, PhoneNumberFormat.INTERNATIONAL)
            else:
                raise ValueError("Número de teléfono no válido.")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("El número de teléfono no tiene un formato correcto.")

    @staticmethod
    def obtener_formato_ejemplo(pais):
        try:
            numero = phonenumbers.parse("8005555555", pais)
            return format_number(numero, PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.phonenumberutil.NumberParseException:
            return "Formato no disponible para el país proporcionado."


class SedeManager:
    def __init__(self, file_path="gestion/datos_universidad.py"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self._save_data({"sedes_registradas": []})

    def _load_data(self):
        try:
            with open(self.file_path, "r") as file:
                file_content = file.read()
                if not file_content.strip():
                    return {"sedes_registradas": []}
                local_variables = {}
                exec(file_content, {}, local_variables)
                sedes = local_variables.get("sedes_registradas", [])
                return {"sedes_registradas": sedes if isinstance(sedes, list) else []}
        except FileNotFoundError:
            return {"sedes_registradas": []}
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return {"sedes_registradas": []}

    def _save_data(self, data):
        try:
            with open(self.file_path, "w") as file:
                file.write(f"sedes_registradas = {data['sedes_registradas']}")
        except Exception as e:
            print(f"Error al guardar datos: {e}")

    def add_sede(self, sede):
        data = self._load_data()
        sedes = data.get("sedes_registradas", [])
        if not isinstance(sedes, list):
            sedes = []
        if any(existing_sede["id_sede"] == sede.id_sede for existing_sede in sedes):
            print(f"Ya existe una sede con ID: {sede.id_sede}")
            return
        else:
            sedes.append(sede.to_dict())
            data["sedes_registradas"] = sedes
            self._save_data(data)
            print(f"Sede {sede.nombre} añadida correctamente.")

    def list_sedes(self):
        try:
            data = self._load_data()
            sedes_data = data.get("sedes_registradas", [])
            if not sedes_data:
                print("No hay sedes registradas.")
                return []

            sedes = [SedeUniversitaria.from_dict(sede) for sede in sedes_data]

            sedes_formateadas = [
                {
                    "id_sede": sede.id_sede,
                    "nombre": sede.nombre,
                    "direccion": sede.direccion,
                    "telefono": sede.telefono,
                }
                for sede in sedes
            ]

            self._print_sedes_user(sedes_formateadas)

        except Exception as e:
            print(f"Error al listar sedes: {e}")
            return []

    def _print_sedes_user(self, sedes):
        if not sedes:
            print("No hay sedes registradas.")
            return

        print("\n" + "=" * 50)
        print("Lista de sedes registradas".center(50))
        print("=" * 50)
        print(f"{'ID Sede':<10} {'Nombre':<30} {'Dirección':<40} {'Teléfono':<20}")
        print("-" * 50)

        for sede in sedes:
            print(
                f"{sede['id_sede']:<10} {sede['nombre']:<30} {sede['direccion']:<40} {sede['telefono']:<20}"
            )

        print("=" * 50)

    def get_sede_by_id(self, id_sede):
        data = self._load_data()
        sedes = data.get("sedes_registradas", [])
        for sede in sedes:
            if sede["id_sede"] == id_sede:
                return sede
        return None

    def get_all_sedes(self):
        try:
            data = self._load_data()
            sedes_data = data.get("sedes_registradas", [])
            if not sedes_data:
                pass
                return []
        except Exception as e:
            print(f"Error al obtener sedes: {e}")
            return []

    def update_sede(self, id_sede, nombre=None, direccion=None, telefono=None):
        data = self._load_data()
        sedes = data.get("sedes_registradas", [])
        for sede in sedes:
            if sede["id_sede"] == id_sede:
                if nombre:
                    sede["nombre"] = nombre
                if direccion:
                    sede["direccion"] = direccion
                if telefono:
                    sede["telefono"] = telefono
                data["sedes_registradas"] = sedes
                self._save_data(data)
                print(f"Sede {id_sede} actualizada correctamente.")
                return
        print(f"Sede con ID {id_sede} no encontrada.")

    def delete_sede(self, id_sede):
        try:
            data = self._load_data()
            sedes = [
                sede
                for sede in data.get("sedes_registradas", [])
                if sede["id_sede"] != id_sede
            ]
            if len(sedes) == len(data.get("sedes_registradas", [])):
                print(f"No se encontró ninguna sede con el ID {id_sede}.")
                return False

            data["sedes_registradas"] = sedes
            self._save_data(data)

            delete_id = str(uuid.uuid4())
            delete_entry = {
                "id": delete_id,
                "id_sede": id_sede,
                "accion": "eliminacion",
                "detalle": f"Sede con ID {id_sede} eliminada.",
                "fecha": str(datetime.datetime.now()),
            }

            dir_path = "gestion/db_sys/"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            file_path = os.path.join(dir_path, "registro_eliminaciones_sedes.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    registros = json.load(f)
            else:
                registros = []

            registros.append(delete_entry)

            with open(file_path, "w") as f:
                json.dump(registros, f, indent=4)

            print(f"Sede {id_sede} eliminada correctamente.")
            return True
        except Exception as e:
            print(f"Error al eliminar sede {id_sede}: {e}")
            return False


def pedir_numero_telefono():
    pais = input(
        "Ingrese el código del país (por ejemplo, 'US' para Estados Unidos): "
    ).upper()

    ejemplo_formato = SedeUniversitaria.obtener_formato_ejemplo(pais)

    if ejemplo_formato == "Formato no disponible para el país proporcionado.":
        print(f"Error: No se encontró un formato adecuado para el país '{pais}'.")
        return pedir_numero_telefono()

    telefono = input(
        f"Ingrese el número de teléfono para {pais} (ejemplo de formato: {ejemplo_formato}): "
    )

    try:
        telefono_formateado = SedeUniversitaria.format_telefono(telefono, pais)
        print(f"Número de teléfono formateado: {telefono_formateado}")
        return telefono_formateado
    except ValueError as e:
        print(f"Error: {e}")
        return pedir_numero_telefono()
