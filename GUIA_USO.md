# 🚀 GUIA DE USO - Sistema de Monografias

## 📋 **COMO RODAR O SISTEMA**

### **1. O servidor já está rodando!**
- **URL**: http://127.0.0.1:8000 ou http://localhost:8000
- **Status**: ✅ Ativo e funcionando

### **2. Credenciais de Acesso**

#### **🔑 Administrador (Superusuário)**
- **Usuário**: `admin`
- **Senha**: `admin123`
- **Acesso**: Total ao sistema

#### **👨‍🏫 Professores (Já cadastrados)**
- **fernando** - Professor/Orientador
- **MaicoDouglas** - Professor/Orientador

#### **👨‍🎓 Alunos (Já cadastrados)**
- **aluno1** - Aluno
- **osiel.junior** - Aluno  
- **rofm** - Aluno

#### **👨‍🎓 Novo Usuário (Criar via interface)**
- Acesse: http://127.0.0.1:8000/accounts/signup/
- Selecione tipo: "Professor" ou "Aluno"
- Preencha os dados

## 🎯 **FUNCIONALIDADES DISPONÍVEIS**

### **📊 Dashboard Principal**
- **URL**: http://127.0.0.1:8000/
- **Funcionalidades**:
  - Estatísticas de monografias
  - Monografias recentes
  - Ações rápidas
  - Estatísticas administrativas (apenas para admins)

### **📚 Gerenciar Monografias**
- **URL**: http://127.0.0.1:8000/monografias/
- **Funcionalidades**:
  - Listar todas as monografias
  - Busca avançada
  - Filtros por status e orientador
  - Ordenação por data/título
  - Paginação

### **➕ Nova Monografia**
- **URL**: http://127.0.0.1:8000/monografias/nova/
- **Permissão**: Professores, Alunos e Administradores
- **Campos obrigatórios**:
  - Título (mínimo 10 caracteres)
  - Resumo (mínimo 100 caracteres)
  - Palavras-chave (mínimo 3 palavras)
  - Autor (aluno)
  - Orientador (professor)
  - Status
  - Data da defesa
  - Arquivo PDF (opcional)

### **👁️ Visualizar Monografia**
- **URL**: http://127.0.0.1:8000/monografias/{id}/
- **Funcionalidades**:
  - Detalhes completos
  - Download do PDF
  - Histórico de revisões
  - Informações da banca

### **✏️ Editar Monografia**
- **URL**: http://127.0.0.1:8000/monografias/{id}/editar/
- **Permissão**: Apenas Professores (suas orientações) e Administradores
- **Funcionalidades**:
  - Editar todos os campos
  - Substituir arquivo PDF
  - Controle de histórico

### **🗑️ Excluir Monografia**
- **URL**: http://127.0.0.1:8000/monografias/{id}/excluir/
- **Permissão**: Apenas Administradores
- **Funcionalidades**:
  - Confirmação de exclusão
  - Remoção permanente

### **⚙️ Interface Administrativa**
- **URL**: http://127.0.0.1:8000/admin/
- **Permissão**: Apenas Administradores
- **Funcionalidades**:
  - Gerenciar usuários
  - Gerenciar monografias
  - Visualizar auditoria
  - Configurações do sistema

## 🔍 **FUNCIONALIDADES DE BUSCA**

### **Busca por Texto**
- Título da monografia
- Nome do autor
- Nome do orientador
- Palavras-chave
- Conteúdo do resumo
- Conteúdo do abstract

### **Filtros Disponíveis**
- **Status**: Em andamento, Submetida, Aprovada, Reprovada
- **Orientador**: Filtro por nome do orientador
- **Data**: Ordenação por data de criação ou defesa

### **Ordenação**
- Data (mais recente/mais antiga)
- Título (A-Z / Z-A)
- Data da defesa

## 👥 **CONTROLE DE ACESSO**

### **🔑 Administradores**
- ✅ Acesso total ao sistema
- ✅ Podem criar, editar e excluir qualquer monografia
- ✅ Visualizam todas as estatísticas
- ✅ Acesso à interface administrativa
- ✅ Podem gerenciar usuários

### **👨‍🏫 Professores**
- ✅ Podem criar monografias
- ✅ Podem editar apenas monografias que orientam
- ✅ Visualizam apenas suas orientações
- ❌ Não podem excluir monografias
- ❌ Não têm acesso ao admin

### **👨‍🎓 Alunos**
- ✅ Podem criar monografias
- ✅ Visualizam apenas suas próprias monografias
- ❌ Não podem editar monografias
- ❌ Não podem excluir monografias
- ❌ Não têm acesso ao admin

## 📝 **VALIDAÇÕES IMPLEMENTADAS**

### **Senhas**
- Mínimo 8 caracteres
- Pelo menos uma letra maiúscula
- Pelo menos uma letra minúscula
- Pelo menos um número
- Pelo menos um caractere especial
- Não pode ser similar ao nome de usuário

### **Arquivos PDF**
- Apenas arquivos PDF
- Máximo 10MB
- Verificação de integridade do arquivo
- Validação do header PDF

### **Formulários**
- Título: 10-200 caracteres
- Resumo: 100-2000 caracteres
- Abstract: mínimo 50 caracteres (se preenchido)
- Palavras-chave: mínimo 3 palavras
- Data da defesa: não pode ser no passado
- Orientador e coorientador devem ser diferentes

## 🚀 **PRÓXIMOS PASSOS**

1. **Acesse o sistema**: http://127.0.0.1:8000
2. **Faça login** com as credenciais do admin
3. **Explore o dashboard** para ver as estatísticas
4. **Crie usuários** (professores e alunos) via cadastro
5. **Cadastre monografias** através do menu
6. **Teste a busca** e filtros
7. **Visualize detalhes** das monografias
8. **Acesse o admin** para gerenciamento avançado

## 🆘 **SOLUÇÃO DE PROBLEMAS**

### **Erro de Conexão**
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo .env

### **Erro de Permissão**
- Verifique se o usuário tem o tipo correto
- Administradores têm acesso total
- Professores só veem suas orientações
- Alunos só veem suas próprias monografias

### **Erro de Upload**
- Verifique se o arquivo é PDF
- Confirme se o tamanho é menor que 10MB
- Teste com um arquivo PDF válido

---

**🎉 Sistema 100% funcional e pronto para uso!**
