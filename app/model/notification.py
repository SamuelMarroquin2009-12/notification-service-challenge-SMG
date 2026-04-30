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