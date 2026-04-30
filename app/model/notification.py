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
