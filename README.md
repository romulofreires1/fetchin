
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

## Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.