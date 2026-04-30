# DESIGN.md - Sistema de Notificaciones y Reportes
## 1. Abstracción del Canal de Notificación
Se ha optado por implementar la abstracción `NotificationChannel` utilizando la clase abstracta `ABC` del módulo `abc` (Tipado Nominal). La decisión se justifica en que un sistema de notificaciones de nivel empresarial se beneficia de contratos estrictos en tiempo de desarrollo e importación. Obligar a las clases a heredar de la base asegura que la jerarquía esté claramente definida y que Python rechace tempranamente la instanciación de cualquier canal mal implementado, reduciendo errores silenciosos.
## 2. Diseño e Integración de DeliveryReport
**Decisión de diseño:**
La clase `DeliveryReport` se ha implementado utilizando el decorador `@dataclass(frozen=True)`. Esta decisión se basa en el principio de inmutabilidad: un reporte es una "fotografía" o registro histórico de lo que sucedió en una sesión. Una vez que el reporte se genera, sus datos no deben cambiar, incluso si el `NotificationService` continúa enviando más mensajes. Ser un objeto inmutable protege la integridad del informe.
**Atributos de la clase:**
*   `channel_name` (str): Identifica el medio por el cual se generó el reporte.
*   `attempted_messages` (int): Total de mensajes que se intentaron enviar en una transacción.
*   `delivered_count` (int): Total de mensajes que se lograron enviar exitosamente.
*   `delivered_messages` (list[str]): Detalle exacto de los textos entregados.
*   `success_rate` (property): Método calculado que retorna un porcentaje (float). Encapsula la lógica matemática evitando que se asigne manualmente un valor incorrecto.
**Integración con NotificationService:**
Para acoplar orgánicamente este reporte, se ha agregado el método `generate_report(attempted: int)` a la clase `NotificationService`. El servicio delega la información de su estado interno (`_channel` y la longitud/copia de `_history`) al constructor del reporte. Se extrae una copia superficial del historial (`self.get_history()`) para garantizar que la lista dentro de `DeliveryReport` no mute por referencia si el servicio sigue procesando datos posteriores a la generación del informe. De esta forma respetamos el principio de Responsabilidad Única (SRP): el servicio se encarga de enviar, y el reporte exclusivamente de empaquetar y mostrar los resultados.