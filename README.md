# Conversor Serasa PDF para CSV

## Descrição

Este projeto tem como objetivo converter um arquivo PDF do Serasa em um arquivo CSV para validação no APEX Crédito e Cobrança.

[Link para app em produção](http://192.168.1.20:5050)

## Como executar localmente

> **OBS: Esse projeto foi desenvolvido visando rodar em um ambiente Linux. Caso esteja utilizando Windows, algumas etapas podem ser diferentes (tente por sua conta e risco).**

0. Certifique-se de ter instalado em seu computador o [Python](https://www.python.org/downloads/), [Pip](https://pip.pypa.io/en/stable/installation/), [Git](https://git-scm.com/downloads) e [Docker](https://www.docker.com/products/docker-desktop).

1. Clone o repositório

```bash
git clone https://github.com/dev-cda/serasa_pdf_to_csv.git
```

2. Acesse a pasta do projeto

```bash
cd serasa_pdf_to_csv
```

3. Rode o comando para buildar o container

```bash
docker-compose build
```

4. Rode o comando para subir o container

```bash
docker-compose up
```

5. Acesse a aplicação no link http://localhost:5000 no seu navegador.

## Como subir atualizações

Para subir atualizações no projeto, devemos primeiro atualizar o repositório local, subir para o repositório remoto (GitHub Dev-CDA) e depois atualizar o repositório que fica no servidor do Docker (192.168.1.20)

Então, após dar commit no seu repositório local e subir para o repositório remoto, siga os passos abaixo:

1. Acesse o servidor do Docker via SSH utilizando as credenciais de acesso.

2. Acesse a pasta do projeto

```bash
cd ..
cd docker
cd serasa_pdf_to_csv
```

3. Identifique e finalize o container que está rodando a aplicação

Para visualizar os containers rodando.

```bash
docker ps
```

Para parar um determinado container. Substitua `<container_id>` pelo ID do container que deseja parar.

```bash
docker stop <container_id>
```

4. Atualize o repositório do servidor com as mudanças feitas no repositório

````bash
git pull
````

5. Refaça o build e suba o container novamente

```bash
docker-compose build
docker-compose up
```

6. Acesse a aplicação no [link](http://192.168.1.20:5050) de produção.