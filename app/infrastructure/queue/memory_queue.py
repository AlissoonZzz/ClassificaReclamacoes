import collections
import json

class MemoryQueue:
    """Uma fila em memória para simular um message broker como RabbitMQ."""
    def __init__(self):
        # Usamos um deque que é otimizado para appends e pops em ambas as pontas
        self._queue = collections.deque()

    def publish(self, message: dict):
        """Publica uma mensagem na fila (simula o produtor)."""
        print(f"INFO: Publicando mensagem na fila: {message}")
        self._queue.append(json.dumps(message))

    def get_message(self) -> str | None:
        """Consome uma mensagem da fila (simula o consumidor)."""
        if not self._queue:
            return None
        
        message = self._queue.popleft()
        print(f"INFO: Mensagem consumida da fila: {message}")
        return message

# Instância da fila que será usada pela aplicação
queue_instance = MemoryQueue()
