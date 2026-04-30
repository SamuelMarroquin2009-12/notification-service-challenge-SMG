# app/model/notification.py

import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
#1 Excepciones personalizadas
class NotificationError(Exception):
    pass
class ChannelUnavailableError(NotificationError):
    pass
class DeliveryError(NotificationError):
    pass
#2 Abstracción NotificationChannel (Opción B)
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
# 3 Implementaciones de la abstracción
class ConsoleChannel(NotificationChannel):
    def is_available(self) -> bool:
        return True
    def get_channel_name(self) -> str:
        return "console"
    def send(self, message: str) -> None:
        if not self.is_available():
            raise ChannelUnavailableError("El canal de consola no está disponible.")
        try:
            print(message, file=sys.stdout)
        except OSError as e:
            raise DeliveryError(f"Error de I/O en consola: {e}")
class FileChannel(NotificationChannel):
    def __init__(self, file_path: str):
        self.file_path = file_path
    def is_available(self) -> bool:
        if os.path.exists(self.file_path):
            return os.access(self.file_path, os.W_OK)
        parent_dir = os.path.dirname(self.file_path) or "."
        return os.path.exists(parent_dir) and os.access(parent_dir, os.W_OK)
    def get_channel_name(self) -> str:
        return f"file:{self.file_path}"
    def send(self, message: str) -> None:
        if not self.is_available():
            raise ChannelUnavailableError(f"No hay permisos o el directorio no existe para: {self.file_path}")
        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except OSError as e:
            raise DeliveryError(f"Fallo al escribir en el archivo: {e}")
class MockChannel(NotificationChannel):
    def is_available(self) -> bool:
        return False

    def get_channel_name(self) -> str:
        return "mock"

    def send(self, message: str) -> None:
        # Se lanza directamente como indica el requerimiento
        raise ChannelUnavailableError("MockChannel nunca está disponible.")
#PARTE2:Propuesta de Clase Adicional
@dataclass(frozen=True)
class DeliveryReport:
    channel_name: str
    attempted_messages: int
    delivered_count: int
    delivered_messages: list[str]
    @property
    def success_rate(self) -> float:
        if self.attempted_messages == 0:
            return 0.0
        return (self.delivered_count / self.attempted_messages) * 100.0