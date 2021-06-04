# Desafio Finxi MVP

O desafio é desenvolver uma pequena aplicação que possibilite a publicação de cotações de peças específicas de droids..

### O que foi usado

- Django
- Django Rest Framework
- Postman
- Docker


### Executando o programa usando Docker Compose

Antes de mais nada, clone o repositório.

``
git clone https://github.com/felipefoc/DesafioFinxi
``

Entre na pasta do projeto

``
cd DesafioFinxi
``

e execute o comando do docker-compose

``
docker-compose up
``

#### Para executar os testes

``
docker exec -it {container_id} python manage.py test
``

- ### Executando o programa com pipenv

Na pasta do projeto, execute o comando

```
pipenv install
```
para instalar as dependências
```
pipenv shell
```
para ativar a virtualenv, após isso execute as migrations
```
python manage.py makemigrations
```
efetue o migrate
```
python manage.py migrate
```
carregue os dados para o banco de dados
```
python manage.py loaddata data.json
```
e inicie o servidor
```
python manage.py runserver
```
