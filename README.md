# Acadefica - Backend
​
Este é o backend para a startup ACADEFICA, que utiliza Machine Learning (IA) para prever e reduzir a evasão de alunos em academias.

O projeto foi desenvolvido em Python utilizando FastAPI e Uvicorn para a criação de API's, Pandas para análise de dados e um Jupyter Notebook para o desenvolvimento e execução do pipeline de IA.

## Tecnologias Utilizadas

O projeto foi construído utilizando as seguintes tecnologias:

- **Python 3**: Linguagem de programação principal.
- **FastAPI**: Framework web para a construção da API.
- **Uvicorn**: Servidor ASGI para rodar a aplicação FastAPI.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Scikit-learn**: Ferramenta para modelagem de machine learning (Regressão Logística e Árvore de Decisão).
- **CTGAN**: Biblioteca para geração de dados sintéticos, utilizada para aumentar a base de treinamento.
- **Papermill**: Ferramenta para executar e parametrizar Jupyter Notebooks.
- **Jupyter Notebook**: Utilizado para o desenvolvimento e execução do pipeline de IA.

## Configuração e Instalação

Siga os passos abaixo para configurar o ambiente e instalar as dependências necessárias.

### Pré-requisitos

- Python 3.8 ou superior
- `pip` (gerenciador de pacotes do Python)

### 1. Clone o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd empreendAcademiaBack
```

### 2. Crie e Ative um Ambiente Virtual

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python3 -m venv .venv

# Ativar o ambiente virtual (Linux/macOS)
source .venv/bin/activate

# Ativar o ambiente virtual (Windows)
.venv\Scripts\activate
```

### 3. Instale as Dependências

Com o ambiente virtual ativado, instale as bibliotecas Python necessárias.

```bash
pip install fastapi uvicorn pandas scikit-learn ctgan papermill "ipykernel<7"
```

**Nota sobre o PyTorch (dependência do CTGAN):**
A biblioteca `ctgan` depende do `torch`. Para evitar a instalação de pacotes pesados de CUDA (GPU), recomendamos instalar a versão para CPU:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install ctgan
```

### 4. Configure o Kernel do Jupyter

O `papermill` precisa de um kernel do Jupyter para executar o notebook. Crie um kernel associado ao seu ambiente virtual:

```bash
python -m ipykernel install --user --name empreend-academia-back
```

### 5. Configure a Tag de Parâmetros no Notebook
​
Para que o `papermill` possa passar o caminho do arquivo de dados para o notebook, a célula correta precisa ser marcada.

1.  Abra o arquivo `ias/iaPipeline.ipynb` em um editor de Jupyter (como o VS Code ou Jupyter Lab).
2.  Encontre a célula que contém a linha `input_file = "database.csv"`.
3.  Adicione a tag `parameters` a essa célula. (No VS Code, clique nos três pontos da célula -> "Adicionar Tag de Célula").

## Como Rodar o Projeto

Após a instalação e configuração, você pode iniciar o servidor da API.

### 1. Inicie o Servidor

Com o ambiente virtual ativado, execute o seguinte comando na raiz do projeto:

```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://127.0.0.1:8000`. A opção `--reload` faz com que o servidor reinicie automaticamente após qualquer alteração no código.

### 2. Endpoints da API

A API fornece os seguintes endpoints:

- **`POST /upload-csv`**: Para fazer o upload de um novo arquivo `database.csv`.
- **`POST /run-pipeline`**: Para executar o pipeline de treinamento da IA e gerar as predições.
- **`GET /get-students-predictions`**: Para obter a lista de predições de evasão para todos os alunos.
- **`GET /get-student-prediction?id={id}`**: Para obter a predição de um aluno específico.
- **`GET /get-student-evasion-percentage`**: Para obter a porcentagem geral de alunos com risco de evasão.
- **`GET /get-student-evasion-percentage-per-unit?unit={unit}`**: Para obter a porcentagem de evasão por unidade.
- **`GET /get-students`**: Retorna todos os alunos da base de dados.
- **`GET /get-student-info?id={id}`**: Retorna as informações de um aluno específico.

Você pode acessar a documentação interativa da API (gerada pelo Swagger UI) em `http://localhost:8000/docs`.

## Contribuidores do projeto:
Ana Clara Segal @segalv -> desenvolvimento do Jupyter Notebook incluído nesse projeto

Giovanna Albuquerque @giabq -> desenvolvimento do front-end do projeto, disponível em https://github.com/giabq/Acadefica

Guilherme Padun @gpadun -> desenvolvimento do front-end do projeto

Júlia Du Bois -> desenvolvimento do back-end incluído nesse projeto
