![CI](https://github.com/qodatecnologia/labqoda-api/workflows/CI/badge.svg)
---

# Labqoda API

Labqoda API

## Setup

1 - Para gerenciar as versões de python e a criação de virtualenvs, instale essas duas ferramentas:

- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)


2 - Verifique a versão corrente do projeto no arquivo .python-version e instale caso necessário

```bash
pyenv install <version>
```

3 - Crie um virtualenv para o projeto

```bash
pyenv virtualenv labqoda
```

4 - Ative o virtualenv

```bash
pyenv activate labqoda
```

5 - Instale as dependencias do projeto

```
make dev-dependencies
```


## Gerando uma nova versão de projeto.

1 - Instale o [nvm](https://github.com/nvm-sh/nvm)

2 - Habilite a versão de node para o projeto com o comando `nvm`

3 - Instale as dependências de node para o projeto

```
npm install
```

4 - Gere uma nova versão do projeto seguindo os passos do `release-it` e o padrão do [semver](https://semver.org/)

```
npx release-it
```


## Acessando documentação da API (swagger).

1 - Para acessar locamente a documentação, rode o seguinte comando para executar o servidor de produção:

```
make run-dev
```

2 - A documentação estará acessível pelo endpoint: [http://localhost:8000/docs/](http://localhost:8000/docs/)
