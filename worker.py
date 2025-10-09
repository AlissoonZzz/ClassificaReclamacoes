import json
import pika
import time

from app.domain.models import Canal
from app.application.use_cases.processar_reclamacao import ProcessarReclamacaoUseCase
from app.application.services.keyword_classification_service import keyword_classification_service_instance
from app.infrastructure.queue.rabbitmq_queue import RabbitMQQueue
from app.infrastructure.repositories.memory_repository import reclamacao_repository_instance

def main():
    """Processo principal do worker."""
    print("INFO: Worker iniciado com serviço de Palavras-Chave.")

    use_case = ProcessarReclamacaoUseCase(
        classification_service=keyword_classification_service_instance,
        repository=reclamacao_repository_instance
    )

    queue = RabbitMQQueue()

    def callback(ch, method, properties, body):
        """Função executada para cada mensagem consumida da fila."""
        print(f"INFO: Mensagem recebida: {body.decode()}")
        try:
            message_dict = json.loads(body)

            reclamacao_processada = use_case.execute(
                texto_reclamacao=message_dict['texto'],
                canal=Canal(message_dict['canal'])
            )
            print(f"INFO: Classificação resultante: {reclamacao_processada.categorias}")

            # Confirma ao RabbitMQ que a mensagem foi processada com sucesso.
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("INFO: Mensagem processada por Palavras-Chave e salva em memória (ack). ")

        except Exception as e:
            print(f"ERRO: Falha ao processar mensagem: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    while True:
        queue.start_consuming(callback)

if __name__ == "__main__":
    main()