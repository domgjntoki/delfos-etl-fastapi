
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

1. Subir 2 containers com o **PostgreSQL**, (a base de dados alvo e a base de dados fonte).
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

Para realizar as transformações, foram definidos os seguintes sinais:

- **wind_speed_mean**: média da velocidade do vento
- **wind_speed_min**: mínimo da velocidade do vento
- **wind_speed_max**: máximo da velocidade do vento
- **wind_speed_std**: desvio padrão da velocidade do vento
- **power_mean**: média da potência gerada
- **power_min**: mínimo da potência gerada
- **power_max**: máximo da potência gerada
- **power_std**: desvio padrão da potência gerada


## Testando no Dagster

Para testar o processo de transformação no Dagster, você pode configurar os inputs diretamente na interface do Dagster ou usando um arquivo de configuração JSON para rodar o pipeline com dados específicos. Abaixo, um exemplo de como configurar o pipeline de teste com um valor de data:

### Exemplo de Configuração para Teste

Você pode fornecer um valor de entrada para o operador `etl_process`, que é o responsável por realizar o processo de ETL (extração, transformação e carga). Para testar o pipeline com uma data específica, use a seguinte configuração JSON:

```json
{
  "ops": {
    "etl_process": {
      "inputs": {
        "date": {
          "value": "2024-11-10"
        }
      }
    }
  }
}
```

Neste exemplo, a data 2024-11-10 será usada como entrada para o operador etl_process, e o Dagster irá rodar o pipeline utilizando esta data. Você pode modificar o valor da data para testar diferentes cenários de transformação e inserção de dados.

### Como Executar o Teste

1. No painel do Dagster, selecione o pipeline que deseja testar.
2. Vá até a seção de "Run Config" e insira o JSON de configuração de teste.
3. Execute o pipeline para ver o processamento com a data fornecida.

Este processo permite que você teste o pipeline com diferentes entradas e valide os resultados no banco de dados ou nas saídas definidas no pipeline.



## Conclusão

Esse projeto foi feito para demonstrar um fluxo de ETL utilizando o Dagster e integração com o FastAPI e PostgreSQL. O código é modular e escalável, permitindo adicionar novas fontes de dados ou sinais no futuro com facilidade.

