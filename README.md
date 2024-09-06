
# (Proposta em Construção) http-utils

**http-utils** é uma biblioteca simples e eficiente para lidar com requisições HTTP em Python. Ela oferece um logger customizado para monitorar o tráfego HTTP, um modelo de métricas customizado para rastrear o desempenho de requisições e um fetcher para facilitar as chamadas HTTP. Esta biblioteca é ideal para desenvolvedores que desejam ter maior controle e visibilidade sobre suas requisições HTTP e métricas de performance.

## Funcionalidades

- **Logger customizado**: Registra e acompanha detalhes das requisições HTTP e suas respostas de forma estruturada.
- **Modelo de métricas customizado**: Colete métricas de desempenho de suas requisições, como tempo de resposta, status e outros dados úteis.
- **Fetcher simples**: Facilita o envio de requisições HTTP (GET, POST, etc.), integrando-se facilmente ao sistema de métricas e logger.

## Instalação

Instale via pip:

```bash
pip install http-utils
```

## Exemplo de Uso

```python
from http_utils import Fetcher, CustomLogger, Metrics

# Configurando o logger e métricas
logger = CustomLogger()
metrics = Metrics()

# Criando um fetcher
fetcher = Fetcher(logger=logger, metrics=metrics)

# Fazendo uma requisição
response = fetcher.get("https://api.example.com/data")
print(response.json())
```

## Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.
