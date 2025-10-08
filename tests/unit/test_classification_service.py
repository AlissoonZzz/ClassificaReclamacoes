from app.application.services.classification_service import ClassificationService

# Configuração de categorias para os testes
categorias_teste = {
    "acesso": ["acessar", "login", "senha"],
    "aplicativo": ["app", "travando", "erro"],
    "fraude": ["fatura", "nao reconhece divida", "fraude"]
}

def test_classificar_reclamacao_simples():
    """Testa a classificação de uma reclamação com uma única categoria."""
    service = ClassificationService(categorias=categorias_teste)
    texto = "nao consigo fazer login"
    resultado = service.classificar(texto)
    assert resultado == ["acesso"]

def test_classificar_reclamacao_multipla():
    """Testa a classificação de uma reclamação com múltiplas categorias."""
    service = ClassificationService(categorias=categorias_teste)
    texto = "o app está travando e eu nao reconhece divida"
    resultado = service.classificar(texto)
    assert resultado == ["aplicativo", "fraude"]

def test_classificar_reclamacao_sem_match():
    """Testa uma reclamação que não corresponde a nenhuma categoria."""
    service = ClassificationService(categorias=categorias_teste)
    texto = "gostaria de saber meu saldo"
    resultado = service.classificar(texto)
    assert resultado == []

def test_classificar_reclamacao_case_insensitive():
    """Testa se a classificação ignora maiúsculas/minúsculas."""
    service = ClassificationService(categorias=categorias_teste)
    texto = "Problemas com a SENHA"
    resultado = service.classificar(texto)
    assert resultado == ["acesso"]
