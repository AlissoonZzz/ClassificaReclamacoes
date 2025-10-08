import re
from typing import List, Dict

class KeywordClassificationService:
    """Serviço responsável pela classificação de reclamações por palavra-chave."""

    def __init__(self, categorias: Dict[str, List[str]]):
        self._categorias = categorias

    def classificar(self, texto: str) -> List[str]:
        """
        Analisa o texto de uma reclamação e retorna uma lista de categorias aplicáveis.
        """
        texto_normalizado = texto.lower()
        categorias_encontradas = set()

        for categoria, palavras_chave in self._categorias.items():
            for palavra in palavras_chave:
                if re.search(r'\b' + re.escape(palavra.lower()) + r'\b', texto_normalizado):
                    categorias_encontradas.add(categoria)
                    break
        
        return sorted(list(categorias_encontradas))

# Em uma aplicação real, isso viria de um banco de dados ou arquivo de configuração.
categorias_config = {
    "imobiliário": ["credito imobiliario", "casa", "apartamento"],
    "seguros": ["resgate", "capitalizacao", "socorro"],
    "cobrança": ["fatura", "cobrança", "valor", "indevido"],
    "acesso": ["acessar", "login", "senha"],
    "aplicativo": ["app", "aplicativo", "travando", "erro"],
    "fraude": ["fatura", "nao reconhece divida", "fraude"]
}

keyword_classification_service_instance = KeywordClassificationService(categorias=categorias_config)
