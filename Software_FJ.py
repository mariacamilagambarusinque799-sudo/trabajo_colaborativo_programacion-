
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
# Responsable: Estudiante 5
# -----------------------------------------------------


# -----------------------------------------------------
# 3. CLASE ABSTRACTA ENTIDAD
# Responsable: (Camila)

class entidad(ABC):
    def __init__(self, nombre, documento):
        self.nombre = nombre
        self.documento = documento

        @abstractmethod
        def mostrar_informacion(self):
            pass



# -----------------------------------------------------
# 4. CLASE CLIENTE
# Responsable:  (Camila)
# -----------------------------------------------------


# -----------------------------------------------------
# 5. CLASE ABSTRACTA SERVICIO
# Responsable: Estudiante 2
# -----------------------------------------------------


# -----------------------------------------------------
# 6. SERVICIOS ESPECIALIZADOS
# Reserva de salas: Estudiante 2
# Alquiler de equipos: Estudiante 3
# Asesorías: Estudiante 3
# -----------------------------------------------------


# -----------------------------------------------------
# 7. CLASE RESERVA
# Responsable: Estudiante 4
# -----------------------------------------------------


# -----------------------------------------------------
# 8. REGISTRO DE EVENTOS Y ERRORES
# Responsable: Estudiante 5
# -----------------------------------------------------


# -----------------------------------------------------
# 9. FUNCIONES DE GESTIÓN DEL SISTEMA
# Responsable: Estudiante 5
# -----------------------------------------------------


# -----------------------------------------------------
# 10. PROGRAMA PRINCIPAL Y PRUEBAS
# Responsable: Estudiante 4
# -----------------------------------------------------

