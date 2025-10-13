# Sistema de Gerenciamento de Monografias

Sistema desenvolvido para gerenciar o ciclo de vida das monografias do Curso de Sistemas de Informação, implementando autenticação robusta e funcionalidades CRUD completas.

## 🚀 Funcionalidades Implementadas

### ✅ Autenticação e Segurança
- **Sistema de autenticação** com django-allauth
- **Controle de acesso** baseado em permissões (Administradores, Professores, Alunos)
- **Criptografia de senhas** com validações robustas
- **Políticas de senha** avançadas (complexidade, histórico)
- **Sistema de auditoria** para rastrear ações dos usuários
- **Dashboard personalizado** com estatísticas

### ✅ CRUD Completo
- **Criação**: Upload de arquivos PDF com validação
- **Leitura**: Busca avançada por múltiplos critérios
- **Atualização**: Edição com controle de histórico
- **Exclusão**: Remoção com confirmação e permissões

### ✅ Funcionalidades Avançadas
- **Busca inteligente** por título, autor, orientador, palavras-chave
- **Paginação e ordenação** dos resultados
- **Validação de arquivos** PDF com verificação de integridade
- **Histórico de revisões** com simple_history
- **Interface administrativa** completa
- **Controles de permissão** refinados por tipo de usuário

## 🛠️ Tecnologias Utilizadas

- **Django 5.2.7** (última versão)
- **PostgreSQL** (banco de dados)
- **Python 3.11+**
- **django-allauth** (autenticação)
- **simple-history** (auditoria)
- **Bootstrap** (interface)

## 📋 Pré-requisitos

```bash
# Instalar dependências
pip install django==5.2.7
pip install django-allauth
pip install simple-history
pip install psycopg2-binary
pip install python-dotenv
```

## ⚙️ Configuração

1. **Configurar banco de dados PostgreSQL**:
```bash
# Criar arquivo .env na raiz do projeto
DB_NAME=monografias
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=sua_chave_secreta
DEBUG=True
```

2. **Executar migrações**:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Criar superusuário**:
```bash
python manage.py createsuperuser
```

4. **Executar servidor**:
```bash
python manage.py runserver
```

## 👥 Tipos de Usuários

### 🔑 Administradores
- Acesso total ao sistema
- Podem criar, editar e excluir qualquer monografia
- Visualizam estatísticas gerais do sistema
- Acesso à interface administrativa

### 👨‍🏫 Professores
- Podem criar e editar monografias
- Visualizam apenas monografias que orientam
- Podem gerenciar orientações e coorientações

### 👨‍🎓 Alunos
- Visualizam apenas suas próprias monografias
- Não podem criar ou editar monografias
- Acesso limitado ao dashboard

## 🔍 Funcionalidades de Busca

- **Busca por texto**: Título, autor, orientador, palavras-chave, resumo
- **Filtros**: Status, orientador, data
- **Ordenação**: Por data, título, status
- **Paginação**: 10 itens por página

## 📊 Dashboard

### Estatísticas Gerais
- Total de monografias
- Distribuição por status
- Monografias recentes

### Estatísticas Administrativas (apenas para admins)
- Total de usuários
- Número de alunos
- Número de orientadores
- Número de coorientadores

## 🔒 Segurança

### Políticas de Senha
- Mínimo 8 caracteres
- Pelo menos uma letra maiúscula
- Pelo menos uma letra minúscula
- Pelo menos um número
- Pelo menos um caractere especial
- Não pode ser similar ao nome de usuário

### Sistema de Auditoria
- Registro de todas as ações dos usuários
- Captura de IP e user agent
- Histórico de alterações
- Logs de login/logout

## 📁 Estrutura do Projeto

```
tp-sd2/
├── accounts/          # Aplicação de usuários
├── core/             # Aplicação principal
├── monografias/      # Configurações do projeto
├── templates/        # Templates base
├── static/           # Arquivos estáticos
└── manage.py
```

## 🚀 Como Usar

1. **Acesse o sistema**: `http://localhost:8000`
2. **Faça login** ou **cadastre-se**
3. **Navegue pelo dashboard** para ver estatísticas
4. **Gerencie monografias** através do menu
5. **Use a busca** para encontrar monografias específicas
6. **Visualize detalhes** clicando no ícone de olho
7. **Edite monografias** (apenas professores e admins)
8. **Acesse o admin** para gerenciamento avançado

## 📝 Campos Obrigatórios

### Monografia
- Título (mínimo 10 caracteres)
- Resumo (mínimo 100 caracteres)
- Palavras-chave (mínimo 3 palavras)
- Autor (aluno)
- Orientador (professor)
- Status
- Data da defesa

### Aluno
- Nome completo
- Matrícula (única)
- E-mail (único)

### Orientador/Coorientador
- Usuário (professor)
- Titulação
- Área de pesquisa

## 🔧 Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver

# Coletar arquivos estáticos
python manage.py collectstatic
```

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- Documentação do Django
- Interface administrativa (`/admin/`)
- Logs do sistema

---

**Desenvolvido para o Curso de Sistemas de Informação**  
**Sistemas Distribuídos - Prof. Alessandro Vivas Andrade**
