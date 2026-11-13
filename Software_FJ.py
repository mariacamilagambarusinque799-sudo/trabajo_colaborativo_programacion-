
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS
# Y RESERVAS - SOFTWARE FJ

# -----------------------------------------------------
# 1. IMPORTACIÓN DE LIBRERÍAS
# Responsable:(Camila)
from abc import ABC, abstractmethod
import logging
from datetime import datetime
# -----------------------------------------------------
# 2. EXCEPCIONES PERSONALIZADAS
# Responsable: (Camila)

# Error general del sistema: todos los demás errores heredan de este
class SistemaError(Exception):
    pass

# Se usa cuando un dato no es válido
class ValidacionError(SistemaError):
    pass

# Se usa cuando se pide un servicio que no está disponible
class ServicioNoDisponibleError(SistemaError):
    pass

# Se usa cuando una reserva no se puede hacer o está mal
class ReservaInvalidaError(SistemaError):
    pass


# -----------------------------------------------------
# 3. CLASE ABSTRACTA ENTIDAD
# Responsable: (Camila)

# Clase abstracta: sirve de molde para otras clases, no se puede crear un objeto directamente de ella
class Entidad(ABC):
    # Constructor: se ejecuta cada vez que se crea un objeto y recibe los datos básicos
    def __init__(self, nombre, documento):
        # Guarda el nombre dentro del objeto
        self.nombre = nombre
        # Guarda el documento dentro del objeto
        self.documento = documento

    # Marca el método como abstracto: las clases hijas están obligadas a escribirlo
    @abstractmethod
    def mostrar_informacion(self):
        # No hace nada aquí; el contenido lo define cada clase hija
        pass


# -----------------------------------------------------
# 4. CLASE CLIENTE
# Responsable: (Camila)

# Cliente hereda de Entidad
class Cliente(Entidad):
    # Constructor: recibe nombre, documento y correo
    def __init__(self, nombre, documento, correo):
        # Llama al constructor de Entidad para guardar nombre y documento
        super().__init__(nombre, documento)
        # Guarda el correo (pasa por la validación del setter)
        self.correo = correo

    # ----- NOMBRE -----
    # Permite leer el nombre con cliente.nombre
    @property
    def nombre(self):
        # Devuelve el valor guardado en el atributo privado
        return self._nombre

    # Se ejecuta cada vez que se asigna un nombre
    @nombre.setter
    def nombre(self, valor):
        # Rechaza si no es texto o si está vacío
        if not isinstance(valor, str) or not valor.strip():
            raise ValidacionError("El nombre no puede estar vacío")
        # Guarda el nombre sin espacios sobrantes en los extremos
        self._nombre = valor.strip()

    # ----- DOCUMENTO -----
    # Permite leer el documento con cliente.documento
    @property
    def documento(self):
        # Devuelve el valor guardado en el atributo privado
        return self._documento

    # Se ejecuta cada vez que se asigna un documento
    @documento.setter
    def documento(self, valor):
        # Debe ser texto, solo números y entre 6 y 10 dígitos
        if not isinstance(valor, str) or not valor.isdigit() or not 6 <= len(valor) <= 10:
            raise ValidacionError("El documento debe tener solo números, entre 6 y 10 dígitos")
        # Si pasó la validación, lo guarda (queda fuera del if)
        self._documento = valor

    # ----- CORREO -----
    # Permite leer el correo con cliente.correo
    @property
    def correo(self):
        # Devuelve el valor guardado en el atributo privado
        return self._correo

    # Se ejecuta cada vez que se asigna un correo
    @correo.setter
    def correo(self, valor):
        # Debe ser texto, tener una sola @ y un punto después de la @
        if not isinstance(valor, str) or valor.count("@") != 1 or "." not in valor.split("@")[1]:
            raise ValidacionError("El correo no es válido")
        # Si pasó la validación, lo guarda
        self._correo = valor

    # Implementa el método abstracto que exige Entidad
    def mostrar_informacion(self):
        # Devuelve un texto con los datos del cliente
        return f"Cliente: {self.nombre} | Documento: {self.documento} | Correo: {self.correo}"


# -----------------------------------------------------
# 5. CLASE ABSTRACTA SERVICIO
# Responsable: (Camila)

# Clase adstracta: molde para los servicios
class Servicio(ABC):
    #contructor: recibe el nombre del servicio y tarifa por hora
    def __init__(self, nombre, tarifa_hora):
        #pasa por la validacion
        self.nombre = nombre
        self.tarifa_hora = tarifa_hora
        #nombre
        @property
        def nombre(self):
            #devuelve el nombre guardado
            return self._nombre
        @nombre.setter
        def nombre(self, valor):
            #rechaza si no hay texto o esta vacio
            if not isinstance(valor, str) or not valor.strip():
                raise ValidacionError("El nombre del servicio no puede estar vacio ")
            # guarda el nombre sin espacios 
            self._nombre = valor.strip()

            #tarifa por hora
            @property
            def tarifa_hora(self):
                #devuelve la tarifa guardada
                return self._tarifa_hora
            @tarifa_hora.setter
            def tarifa_hora(self,valor):
                #debe ser un numero mayor que cero 
                if not isinstance(valor, (int, float)) or valor <= 0:
                    raise ValidacionError("la tarifa por hora debe ser un numero mayor que cero")
                #guarda la tarifa
                self._tarifa_hora = valor

                #metodo adstracto: cada servicio calcula su costo base a su manera 
                @abstractmethod
                def calcular_costo(self, horas):
                    pass
                #cada servicio se describe a su manera
                @abstractmethod
                def describir(self):
                    pass
                # cada servicio valida sus propios parametros
                    @abstractmethod
                    def validar_parametros(self, horas):
                         pass

    # Método sobrecargado: el mismo cálculo con impuesto y descuento opcionales
    def calcular_costo_total(self, horas, impuesto=0, descuento=0):
        # Costo base según el servicio 
        costo = self.calcular_costo(horas)
        # Aplica el descuento 
        costo = costo - costo * descuento
        # Aplica el impuesto 
        costo = costo + costo * impuesto
        # Devuelve el costo final
        return costo
# -----------------------------------------------------
# 6. SERVICIOS ESPECIALIZADOS
# Reserva de salas: Estudiante 2
# Alquiler de equipos: Estudiante 3
# Asesorías: Estudiante 3



# -----------------------------------------------------
# 7. CLASE RESERVA
# Responsable: Estudiante 4



# -----------------------------------------------------
# 8. REGISTRO DE EVENTOS Y ERRORES
# Responsable: Estudiante 5



# -----------------------------------------------------
# 9. FUNCIONES DE GESTIÓN DEL SISTEMA
# Responsable: Estudiante 5



# -----------------------------------------------------
# 10. PROGRAMA PRINCIPAL Y PRUEBAS
# Responsable: Estudiante 4


