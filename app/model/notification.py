import os
from abc import ABC, abstractmethod
# 1. Excepciones personalizadas muy básicas
class NotificationError(Exception):
    pass
class ChannelUnavailableError(NotificationError):
    pass
class DeliveryError(NotificationError):
    pass
# 2. Abstracción del canal (Opción B, clásica y directa)
class NotificationChannel(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass
    @abstractmethod
    def get_channel_name(self) -> str:
        pass
    @abstractmethod
    def is_available(self) -> bool:
        pass
# 3. Implementaciones
class ConsoleChannel(NotificationChannel):
    def is_available(self) -> bool:
        return True  # Siempre está listo
    def get_channel_name(self) -> str:
        return "console"
    def send(self, message: str) -> None:
        if self.is_available() == False:
            raise ChannelUnavailableError("La consola no se puede usar.")
        try:
            print(message)
        except Exception:
            raise DeliveryError("Hubo un problema raro al imprimir en pantalla.")
class FileChannel(NotificationChannel):
    def __init__(self, file_path: str):
        self.file_path = file_path
    def is_available(self) -> bool:
        carpeta = os.path.dirname(self.file_path)
        if carpeta == "":
            carpeta = "."
        if os.path.exists(self.file_path):
            return os.access(self.file_path, os.W_OK)
        else:
            return os.path.exists(carpeta) and os.access(carpeta, os.W_OK)
    def get_channel_name(self) -> str:
        return "file:" + self.file_path
    def send(self, message: str) -> None:
        if self.is_available() == False:
            raise ChannelUnavailableError("No tienes permisos para escribir en este archivo.")
        try:
            archivo = open(self.file_path, "a")
            archivo.write(message + "\n")
            archivo.close()
        except Exception:
            raise DeliveryError("Algo falló mientras se guardaba el texto.")
class MockChannel(NotificationChannel):
    def is_available(self) -> bool:
        return False  # Nunca funciona, es de mentiritas
    def get_channel_name(self) -> str:
        return "mock"
    def send(self, message: str) -> None:
        raise ChannelUnavailableError("Este canal es de prueba y siempre falla.")
# Parte 2: Propuesta de Clase Adicional
class DeliveryReport:
    def __init__(self, channel_name: str, attempted: int, delivered_messages: list[str]):
        self.channel_name = channel_name
        self.attempted_messages = attempted
        self.delivered_messages = delivered_messages
        self.delivered_count = len(delivered_messages)
    def get_success_rate(self) -> float:
        if self.attempted_messages == 0:
            return 0.0
        return (self.delivered_count / self.attempted_messages) * 100.0
# 4. Clase NotificationService
class NotificationService:
    def __init__(self, channel: NotificationChannel):
        self._channel = channel
        self._history: list[str] = []  # Empezamos con la lista vacía
    def send_notification(self, message: str) -> None:
        if self._channel.is_available() == False:
            raise ChannelUnavailableError("El canal está apagado o roto.")
        self._channel.send(message)
        self._history.append(message)
    def send_bulk(self, messages: list[str]) -> int:
        exitosos = 0
        for mensaje in messages:
            try:
                self.send_notification(mensaje)
                exitosos = exitosos + 1
            except NotificationError:
                pass
        return exitosos
    def get_history(self) -> list[str]:
        return list(self._history)
    def generate_report(self, attempted: int) -> DeliveryReport:
        return DeliveryReport(
            channel_name=self._channel.get_channel_name(),
            attempted=attempted,
            delivered_messages=self.get_history()
        )