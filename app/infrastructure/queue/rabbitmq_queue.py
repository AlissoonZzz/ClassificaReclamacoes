import pika
import json
import time

import os

class RabbitMQQueue:
    def __init__(self, queue_name='reclamacoes_queue'):
        self._host = os.environ.get("RABBITMQ_HOST", "localhost")
        self._queue_name = queue_name

    def publish(self, message: dict):
        """Cria uma conexão, publica uma mensagem e fecha a conexão."""
        connection = None
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
            channel = connection.channel()
            channel.queue_declare(queue=self._queue_name, durable=True)
            channel.basic_publish(
                exchange='',
                routing_key=self._queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            print(f"INFO: Mensagem publicada na fila '{self._queue_name}': {message}")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"ERRO: API não conseguiu conectar ao RabbitMQ em '{self._host}'.")
            raise
        finally:
            if connection and connection.is_open:
                connection.close()

    def start_consuming(self, callback):
        """Inicia o consumo de mensagens da fila (usado apenas pelo worker)."""
        connection = None
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host, heartbeat=600))
            channel = connection.channel()
            channel.queue_declare(queue=self._queue_name, durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=self._queue_name, on_message_callback=callback)
            
            print(f"INFO: Aguardando mensagens na fila '{self._queue_name}'. Para sair pressione CTRL+C")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"ERRO: Worker não conseguiu conectar ao RabbitMQ em '{self._host}'. Tentando novamente em 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("INFO: Consumo interrompido.")
        finally:
            if connection and connection.is_open:
                connection.close()
