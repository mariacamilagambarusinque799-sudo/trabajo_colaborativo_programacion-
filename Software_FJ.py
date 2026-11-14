
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
# ==========================================
# 6. SERVICIOS ESPECIALIZADOS (Polimorfismo)
# ==========================================
def _validar_horas(horas):
    """Las horas deben ser un número mayor que 0."""
    if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:
        raise ValidacionError(f"Las horas deben ser un número mayor que 0 (recibido: {horas!r}).")
    return True


def _validar_entero_positivo(valor, nombre):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise ValidacionError(f"'{nombre}' debe ser un número entero mayor que 0 (recibido: {valor!r}).")


class ReservaSalas(Servicio):
    MAX_HORAS = 12  # una sala no se reserva por más de 12 horas seguidas

    def __init__(self, tarifa_hora, capacidad):
        super().__init__("Reserva de Salas", tarifa_hora)
        _validar_entero_positivo(capacidad, "capacidad")
        self.capacidad = capacidad
        self.disponible = True

    def validar_parametros(self, horas):
        _validar_horas(horas)
        if horas > self.MAX_HORAS:
            raise ValidacionError(f"Una sala no puede reservarse por más de {self.MAX_HORAS} horas.")
        return True

    def calcular_costo(self, horas):
        self.validar_parametros(horas)
        return self.tarifa_hora * horas

    def describir(self):
        return (f"{self.nombre}: capacidad para {self.capacidad} personas, "
                f"${self.tarifa_hora:,.0f} por hora")


class AlquilerEquipos(Servicio):
    def __init__(self, tarifa_hora, cantidad_equipos):
        super().__init__("Alquiler de Equipos", tarifa_hora)
        _validar_entero_positivo(cantidad_equipos, "cantidad_equipos")
        self.cantidad_equipos = cantidad_equipos
        self.disponible = True

    def validar_parametros(self, horas):
        return _validar_horas(horas)

    def calcular_costo(self, horas):
        self.validar_parametros(horas)
        return self.tarifa_hora * horas * self.cantidad_equipos

    def describir(self):
        return (f"{self.nombre}: {self.cantidad_equipos} equipo(s), "
                f"${self.tarifa_hora:,.0f} por hora cada uno")


class AsesoriasEspecializadas(Servicio):
    def __init__(self, tarifa_hora, especialidad):
        super().__init__("Asesorías Especializadas", tarifa_hora)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValidacionError("La especialidad de la asesoría no puede estar vacía.")
        self.especialidad = especialidad.strip()
        self.disponible = True

    def validar_parametros(self, horas):
        return _validar_horas(horas)

    def calcular_costo(self, horas):
        self.validar_parametros(horas)
        return self.tarifa_hora * horas

    def describir(self):
        return (f"{self.nombre} en {self.especialidad}: "
                f"${self.tarifa_hora:,.0f} por hora")


# ==========================================
# 7. CLASE RESERVA
# ==========================================
def _validar_porcentaje(valor, nombre):
    """Impuesto y descuento se expresan entre 0 y 1 (0.19 = 19 %)."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not 0 <= valor <= 1:
        raise ValidacionError(f"El {nombre} debe ser un número entre 0 y 1 (recibido: {valor!r}).")


class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")
        try:
            servicio.validar_parametros(duracion)
        except ValidacionError as e:
            raise ReservaInvalidaError("Duración de la reserva inválida.") from e
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion  # en horas
        self.__estado = "Pendiente"
        self.__costo = None

    # Encapsulación: solo lectura desde afuera
    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo

    def confirmar(self):
        if self.__estado != "Pendiente":
            raise ReservaInvalidaError(f"No se puede confirmar una reserva en estado '{self.__estado}'.")
        self.__estado = "Confirmada"

    def cancelar(self):
        if self.__estado == "Cancelada":
            raise ReservaInvalidaError("La reserva ya estaba cancelada.")
        self.__estado = "Cancelada"

    def procesar(self, impuesto=0, descuento=0):
        """Valida, calcula el costo total y confirma. Devuelve el costo."""
        if self.__estado != "Pendiente":
            raise ReservaInvalidaError(f"Solo se procesan reservas pendientes (estado: '{self.__estado}').")
        try:
            if not getattr(self.__servicio, "disponible", True):
                raise ServicioNoDisponibleError(f"El servicio '{self.__servicio.nombre}' no está disponible.")
            _validar_porcentaje(impuesto, "impuesto")
            _validar_porcentaje(descuento, "descuento")
            self.__servicio.validar_parametros(self.__duracion)
            costo = self.__servicio.calcular_costo_total(self.__duracion, impuesto, descuento)
        except (ValidacionError, ServicioNoDisponibleError) as e:
            self.__estado = "Fallida"
            registrar_log(f"Reserva fallida: {e}", "ERROR")
            raise ReservaInvalidaError("No se pudo procesar la reserva.") from e
        else:
            self.__costo = costo
            self.confirmar()
            registrar_log(f"Reserva confirmada ({self.__servicio.nombre}) para "
                          f"{self.__cliente.nombre}. Costo: ${costo:,.0f}")
            return costo
        finally:
            registrar_log(f"Fin del procesamiento. Estado final: {self.__estado}.", "DEBUG")


# ==========================================
# 8. REGISTRO DE EVENTOS Y ERRORES (LOGS)
# ==========================================
def registrar_log(mensaje, tipo="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{tipo}] {mensaje}\n"
    try:
        with open("sistema_logs.txt", "a", encoding="utf-8") as archivo:
            archivo.write(log_entry)
    except OSError as e:
        # Si falla el log, el sistema sigue funcionando
        print(f"Error al escribir en el archivo de logs: {e}")


# ==========================================
# 9. FUNCIONES DE GESTIÓN Y OPERACIONES
# ==========================================
class ClienteNoEncontradoError(SistemaError):
    """Se busca un cliente que no está registrado."""


def operacion_registrar_cliente(clientes_db, nombre, documento, correo):
    """Registra un cliente (clave = documento). Devuelve el Cliente o None."""
    try:
        if documento in clientes_db:
            raise ValidacionError(f"Ya existe un cliente con documento {documento}.")
        cliente = Cliente(nombre, documento, correo)
    except SistemaError as e:
        registrar_log(f"Registro de cliente fallido: {e}", "ERROR")
        print(f"[X] No se pudo registrar al cliente ({documento}): {e}")
        return None
    else:
        clientes_db[documento] = cliente
        registrar_log(f"Cliente {documento} registrado.")
        print(f"[OK] {cliente.mostrar_informacion()}")
        return cliente
    finally:
        print("    (fin del registro de cliente)")


def operacion_buscar_cliente(clientes_db, documento_buscado):
    """Busca un cliente por documento. Devuelve el Cliente o None."""
    try:
        if documento_buscado not in clientes_db:
            raise ClienteNoEncontradoError(
                f"El cliente con documento {documento_buscado} no está registrado.")
        cliente = clientes_db[documento_buscado]
    except ClienteNoEncontradoError as e:
        registrar_log(str(e), "ADVERTENCIA")
        print(f"[X] Excepción controlada: {e}")
        return None
    else:
        registrar_log(f"Consulta exitosa del cliente {documento_buscado}.")
        print(f"[OK] Cliente encontrado: {cliente.nombre}")
        return cliente
    finally:
        print("    (fin de la validación de cliente)")


def operacion_crear_servicio(clase_servicio, *args):
    """Crea un servicio de forma segura. Devuelve el servicio o None."""
    try:
        servicio = clase_servicio(*args)
    except ValidacionError as e:
        registrar_log(f"Creación de {clase_servicio.__name__} fallida: {e}", "ERROR")
        print(f"[X] Servicio inválido ({clase_servicio.__name__}): {e}")
        return None
    except TypeError as e:  # parámetros faltantes
        registrar_log(f"Parámetros faltantes en {clase_servicio.__name__}: {e}", "ERROR")
        print(f"[X] Parámetros faltantes ({clase_servicio.__name__}): {e}")
        return None
    else:
        registrar_log(f"Servicio creado: {servicio.describir()}")
        print(f"[OK] {servicio.describir()}")
        return servicio
    finally:
        print("    (fin de la creación de servicio)")


def operacion_reservar(cliente, servicio, horas, impuesto=0, descuento=0):
    """Crea y procesa una reserva. Devuelve la Reserva o None."""
    try:
        reserva = Reserva(cliente, servicio, horas)
        costo = reserva.procesar(impuesto, descuento)
    except ReservaInvalidaError as e:
        causa = f" (causa: {e.__cause__})" if e.__cause__ else ""
        registrar_log(f"Reserva no realizada: {e}{causa}", "ERROR")
        print(f"[X] Reserva fallida: {e}{causa}")
        return None
    else:
        print(f"[OK] Reserva {reserva.estado}. Costo total: ${costo:,.0f}")
        return reserva
    finally:
        print("    (fin de la operación de reserva)")


def operacion_cancelar_reserva(reserva):
    try:
        reserva.cancelar()
    except ReservaInvalidaError as e:
        registrar_log(f"Cancelación fallida: {e}", "ADVERTENCIA")
        print(f"[X] No se pudo cancelar: {e}")
    else:
        registrar_log("Reserva cancelada.")
        print(f"[OK] Reserva cancelada (estado: {reserva.estado})")
    finally:
        print("    (fin de la cancelación)")


# ==========================================
# 10. PROGRAMA PRINCIPAL Y PRUEBAS
# ==========================================
def ejecutar_pruebas():
    clientes_db = {}

    print("\n[1] Registro válido de cliente")
    ana = operacion_registrar_cliente(clientes_db, "Ana Pérez", "10203040", "ana@correo.com")

    print("\n[2] Registro inválido: correo sin @")
    operacion_registrar_cliente(clientes_db, "Luis Gómez", "20304050", "correo-sin-arroba")

    print("\n[3] Registro inválido: documento con letras")
    operacion_registrar_cliente(clientes_db, "Marta Ruiz", "12ab", "marta@correo.com")

    print("\n[4] Búsqueda de cliente existente")
    operacion_buscar_cliente(clientes_db, "10203040")

    print("\n[5] Búsqueda de cliente inexistente")
    operacion_buscar_cliente(clientes_db, "99999999")

    print("\n[6] Creación correcta: sala")
    sala = operacion_crear_servicio(ReservaSalas, 50000, 10)

    print("\n[7] Creación incorrecta: sala con tarifa 0")
    operacion_crear_servicio(ReservaSalas, 0, 10)

    print("\n[8] Creación correcta: alquiler de equipos")
    equipos = operacion_crear_servicio(AlquilerEquipos, 20000, 4)

    print("\n[9] Creación incorrecta: asesoría con parámetro faltante")
    operacion_crear_servicio(AsesoriasEspecializadas, 80000)

    print("\n[10] Reserva exitosa (IVA 19 % y 10 % de descuento)")
    reserva = operacion_reservar(ana, sala, 3, impuesto=0.19, descuento=0.10)

    print("\n[11] Reserva fallida: servicio no disponible")
    equipos.disponible = False
    operacion_reservar(ana, equipos, 2)

    print("\n[12] Reserva fallida: sin cliente")
    operacion_reservar(None, sala, 2)

    print("\n[13] Reserva fallida: horas negativas")
    operacion_reservar(ana, sala, -2)

    print("\n[14] Cancelación y cancelación repetida")
    if reserva:
        operacion_cancelar_reserva(reserva)
        operacion_cancelar_reserva(reserva)

    print("\n[15] Asesoría válida + comparación polimórfica (2 horas)")
    asesoria = operacion_crear_servicio(AsesoriasEspecializadas, 80000, "Python")
    equipos.disponible = True
    for s in (sala, equipos, asesoria):
        if s:
            print(f"    {s.nombre}: ${s.calcular_costo(2):,.0f}")


if __name__ == "__main__":
    print("--- INICIANDO SISTEMA SOFTWARE FJ ---")
    registrar_log("Sistema iniciado.")
    try:
        ejecutar_pruebas()
    except Exception as e:  # último recurso: el sistema nunca debe caerse
        registrar_log(f"Error inesperado en el programa principal: {e}", "CRITICO")
        print(f"Error inesperado controlado: {e}")
    finally:
        registrar_log("Sistema finalizado.")
        print("\n--- FIN DEL PROGRAMA ---")