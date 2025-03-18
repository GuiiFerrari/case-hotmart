# case-hotmart

## Descrição

O projeto consiste em um uso simples de uma LLM local, onde é possível armazenar informações da página de uma página da hotmart em um banco de dados vetorial open source, com o objetivo de facilitar a busca de informações sobre a empresa, fornecendo contexto para as perguntas feitas. O projeto conta com dois microsserviços, um para a coleta de dados, usando webscraping, e outro para conseguir fazer perguntas para a LLM.

O primeiro microserviço possui acesso por API feito em FastAPI e pode ser acessado em localhost:5001/. O segundo também possui acesso por API feito em FastAPI e pode ser acessado em localhost:5000/. O banco de dados escolhido foi o [Marqo](https://github.com/marqo-ai/marqo), devido a sua simplicidade e facilidade de uso.

## Como rodar

Para rodar o projeto, é necessário ter o docker e docker-compose instalados. É possível subir toda a aplicação a partir do comando:

```
make run
```

Ou, se preferir rodar sem o uso do Make, basta rodar o comando:

```
docker-compose up -d --build
```

## Como usar

Primeiro, faça o check de que os serviços estão rodando corretamente. Para isso, faça uma requisição GET para os endpoints:

 - localhost:5000/health
 - localhost:5001/health

Ambos devem retornar um JSON com a chave "status" e o valor "ok".

Para o check do banco de dados, basta fazer uma requisição GET para um dos dois endpoints:

- localhost:5000/db/health
- localhost:5001/db/health

Ambos devem retornar um JSON com a chave "status" e o valor "yellow" caso não tenham nenhum dado armazenado, após isso devem retornar "green".

Antes de fazer perguntas referentes a hotmart, faça uma requisição POST para o endpoint http://localhost:5001/fetch_hotmart_info, com o argumento url=https://hotmart.com/pt-br/blog/como-funciona-hotmart. Isso irá preencher o banco de dados com as informações da página.

### Perguntas

Para fazer perguntas, basta fazer uma requisição POST para o endpoint localhost:5000/ask, com o seguinte corpo:

```json
{
    "question": "Qual a capital do Brasil?"
}
```

O retorno será a resposta da LLM, onde para cada pergunta será feita uma busca no bando de dados para enriquecer a pergunta com contexto.

Para exemplos de utilização, utilize o arquivo PostmanCollection.json, que contém exemplos de requisições para os dois microserviços, onde também contém alguns testes de funcionalidade.

