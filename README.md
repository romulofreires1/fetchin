
# http-utils

**http-utils** é uma biblioteca eficiente para lidar com requisições HTTP em Python. Ela oferece um logger customizado para monitorar o tráfego HTTP, um modelo de métricas para rastrear o desempenho das requisições, e um fetcher para facilitar as chamadas HTTP. Esta biblioteca é ideal para desenvolvedores que desejam maior controle e visibilidade sobre suas requisições HTTP e métricas de performance.

## Funcionalidades

- **Logger customizado**: Registra detalhes das requisições HTTP e suas respostas de forma estruturada.
- **Modelo de métricas**: Colete métricas como tempo de resposta, contagem de requisições e status HTTP.
- **Fetcher**: Facilita o envio de requisições HTTP (GET, POST, etc.), com integração com o logger e sistema de métricas.

## Parâmetros do Fetcher

O `Fetcher` aceita os seguintes parâmetros ao ser instanciado:

- **label (str)**: Um rótulo para identificar o fetcher. Fetchers com o mesmo rótulo compartilham o mesmo Circuit Breaker.
- **logger (CustomLogger)**: Logger customizado para registrar as requisições.
- **metrics (MetricsInterface)**: Sistema de métricas (opcional). Se não for passado, o Prometheus será usado por padrão.
- **circuit_config (dict)**: Configurações do Circuit Breaker, incluindo:
  - `fail_max`: Número máximo de falhas antes de abrir o Circuit Breaker.
  - `reset_timeout`: Tempo em segundos para esperar antes de fechar o Circuit Breaker após uma falha.
  - `backoff_strategy`: Estratégia de backoff para determinar o tempo de espera entre retries.
- **max_retries (int)**: Número máximo de tentativas de repetição (retries) para uma requisição em caso de falha.

## Instalação

Instale via pip:

```bash
pip install http-utils
```

## Exemplo de Uso

### Exemplo básico com Prometheus (implementação padrão)

```python
from http_utils.logging.logger import CustomLogger
from http_utils.fetcher.fetcher import Fetcher
from http_utils.metrics.prometheus_metrics import PrometheusMetrics


logger = CustomLogger()

# Configuração do Circuit Breaker com estratégia de backoff linear
def linear_backoff(attempt: int):
    return attempt * 2

circuit_config = {
    "fail_max": 3,
    "reset_timeout": 60,
    "backoff_strategy": linear_backoff
}

# Criando um fetcher usando o logger e o Prometheus como sistema de métricas padrão
fetcher = Fetcher(label="api-service", logger=logger, metrics=PrometheusMetrics(), circuit_config=circuit_config, max_retries=5)

try:
    response = fetcher.get("http://localhost:8080/api/example")
    print(response.json())
except Exception as e:
    logger.error(f"Error during fetch: {e}")
```

### Exemplo com implementação personalizada de métricas

Você também pode fornecer sua própria implementação de métricas. Basta implementar a interface `MetricsInterface`.

```python
from http_utils.logging.logger import CustomLogger
from http_utils.metrics.metrics_interface import MetricsInterface
from http_utils.fetcher.fetcher import Fetcher

class CustomMetrics(MetricsInterface):
    def track_request(self, method: str, status_code: int, response_time: float):
        print(f"Custom Metrics -> Method: {method}, Status: {status_code}, Time: {response_time:.2f}s")
    
    def track_retry(self, method: str):
        print(f"Custom Retry -> Method: {method}")

logger = CustomLogger()
metrics = CustomMetrics()

# Criando um fetcher com implementação personalizada de métricas
fetcher = Fetcher(label="api-service", logger=logger, metrics=metrics, max_retries=3)

try:
    response = fetcher.get("http://localhost:8080/api/example")
    print(response.json())
except Exception as e:
    logger.error(f"Error during fetch: {e}")
```

## Configurando o Ambiente Virtual

Para configurar um ambiente virtual Python e instalar as dependências:

1. Crie o ambiente virtual:

   ```bash
   python3 -m venv venv
   ```

2. Ative o ambiente virtual:

   - **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

3. Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```

4. Para desativar o ambiente virtual, execute:

   ```bash
   deactivate
   ```

## Subindo uma API Mock de Teste

Você pode usar o **WireMock** para subir uma API mock de teste. Com **Docker Compose**, você pode facilmente subir e derrubar a API mock. Veja os passos abaixo:

### Subir a API Mock:

1. Execute o seguinte comando para subir a API mock em segundo plano:

   ```bash
   make docker-up
   ```

2. Agora, a API mock estará disponível em `http://localhost:8080`. Você pode testar um endpoint de exemplo com:

   ```bash
   curl http://localhost:8080/api/example
   ```

   Isso deverá retornar uma resposta mockada como:

   ```json
   {
     "message": "This is a mocked response from WireMock!"
   }
   ```

### Derrubar a API Mock:

Para derrubar a API mock e parar o container, execute:

```bash
make docker-down
```

## Comandos adicionais no Makefile

### Instalar dependências

Para instalar as dependências do projeto, execute:

```bash
make install
```

### Lint do código

Para verificar o estilo do código com o **flake8**, execute:

```bash
make lint
```

### Formatar o código

Para formatar o código de acordo com as convenções de estilo usando **black**, execute:

```bash
make format
```

### Rodar os testes

Para rodar os testes do projeto usando **pytest**, execute:

```bash
make test
```

### Build do Docker Compose

Se houver mudanças nos arquivos de configuração e você quiser fazer o build do container do WireMock, execute:

```bash
make docker-build
```

### Logs do WireMock

Para ver os logs do container do WireMock em tempo real, execute:

```bash
make docker-logs
```

### Playground

Para testar a execução do projeto e ver exemplos de uso no **playground**, execute:

```bash
make play
```

## Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.