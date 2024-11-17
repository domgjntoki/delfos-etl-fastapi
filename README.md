
# Projeto de ETL com Dagster e FastAPI

Este projeto foi desenvolvido como parte de um teste de programação. Ele implementa um processo de ETL (Extract, Transform, Load) utilizando o **Dagster** para orquestrar e automatizar a coleta e processamento de dados. A API **FastAPI** fornece os dados brutos, enquanto o **PostgreSQL** é utilizado para armazenar os resultados agregados.

## Visão Geral

O objetivo principal do projeto é coletar dados de uma API FastAPI e realizar agregações de dados antes de armazená-los em um banco de dados PostgreSQL. O Dagster é responsável por orquestrar as tarefas e garantir a execução automática.

## Como Rodar o Projeto

Para rodar o projeto, utilize o Docker e Docker Compose. Execute o comando abaixo para levantar todos os containers necessários:

```bash
docker compose up -d
```

Esse comando irá:

1. Subir o container com o **PostgreSQL**.
2. Subir o container com o **Dagster**.
3. Subir o container com o **FastAPI** (servindo os dados).
4. Iniciar a execução das tarefas ETL automaticamente, conforme a programação definida no Dagster.

## Passos para Rodar Localmente

1. **Certifique-se de ter o Docker e Docker Compose instalados**.
2. Clone o repositório para o seu ambiente local.
3. Navegue até o diretório do projeto e execute:

   ```bash
   docker compose up -d
   ```

4. Acesse o **Dagster UI** em [http://localhost:3000](http://localhost:3000) para acompanhar o andamento das execuções do ETL.

5. Acesse a **API FastAPI** em [http://localhost:8000](http://localhost:8000) para verificar os endpoints disponíveis.

## Sinais e Agregações Utilizadas

Para realizar as transformações, foram definidos dois sinais principais:

- **wind_speed**: velocidade do vento
- **power**: potência gerada

A seguir estão os tipos de agregação utilizados para cada sinal:

- **mean**: média
- **min**: mínimo
- **max**: máximo
- **std**: desvio padrão

Esses sinais são processados pelo Dagster, que realiza as agregações de 10 em 10 minutos, e os dados são inseridos no banco de dados PostgreSQL na tabela `data`.

## Estrutura do Banco de Dados

O banco de dados PostgreSQL possui duas tabelas principais:

1. **signal**: Armazena os sinais com suas respectivas informações.
    - `id`: Identificador único do sinal (auto-incrementado).
    - `name`: Nome do sinal (exemplo: `wind_speed_mean`).

2. **data**: Armazena os valores agregados de cada sinal.
    - `id`: Identificador único da entrada de dados.
    - `timestamp`: Data e hora do dado agregado.
    - `signal_id`: Relaciona o dado com um sinal específico.
    - `value`: Valor agregado (média, mínimo, máximo ou desvio padrão).

### Estrutura de Tabelas SQL

```sql
CREATE TABLE signal (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    signal_id INT REFERENCES signal(id),
    value FLOAT NOT NULL
);
```

## Conclusão

Esse projeto foi feito para demonstrar um fluxo de ETL utilizando o Dagster e integração com o FastAPI e PostgreSQL. O código é modular e escalável, permitindo adicionar novas fontes de dados ou sinais no futuro com facilidade.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
