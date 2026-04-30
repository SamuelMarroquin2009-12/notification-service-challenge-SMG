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