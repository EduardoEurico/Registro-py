# API - Sistema de Gerenciamento de Heróis, Crimes, Batalhas e Missões

Bem-vindo à API de gerenciamento de heróis, crimes, batalhas e missões! Esta API foi desenvolvida para gerenciar informações de heróis, missões realizadas, crimes combatidos e batalhas entre heróis, inspirada na série *The Boys*. 

---

## Documentação Completa
Para acessar a documentação completa e interativa da API, visite o link abaixo:

[Documentação da API no Postman](https://documenter.getpostman.com/view/36430231/2sAYBUCX5o)

---

## Funcionalidades Principais
### **Administração de Heróis**
- Criação, consulta, atualização e remoção de heróis, com atributos como poderes, nível de força, popularidade e status.

### **Missões**
- Gerenciamento de missões realizadas pelos heróis, incluindo designação de heróis, recompensas e resultados.

### **Crimes**
- Registro e consulta de crimes combatidos pelos heróis, com detalhes como descrição, data e severidade.

### **Batalhas**
- Simulação de batalhas entre heróis, com cálculos de resultados e impacto nos atributos dos personagens.

---

## Como Começar
1. **Registro:** Configure o ambiente da API localmente ou em um servidor.
2. **Autenticação:** Esta versão da API não requer autenticação, mas recomenda-se implementá-la em sistemas reais.
3. **Exploração:** Use a documentação interativa para testar os endpoints e explorar as funcionalidades.

---

## Exemplos de Endpoints

### **Heróis**
- **Adicionar Herói:** `POST /heroes/cadastrar`
- **Listar Heróis:** `GET /heroes`
- **Atualizar Herói:** `PUT /heroes/{id}`
- **Deletar Herói:** `DELETE /heroes/{id}`

### **Missões**
- **Cadastrar Missão:** `POST /missoes/cadastrar`
- **Listar Missões:** `GET /missoes`
- **Buscar Missões por Filtro:** `GET /missoes/{id}?difficulty={difficulty}&hero_id={hero_id}`
- **Deletar Missão:** `DELETE /missoes/deletar/{id}`

### **Crimes**
- **Cadastrar Crime:** `POST /crimes/cadastrar`
- **Listar Crimes:** `GET /crimes`
- **Atualizar Crime:** `PUT /crimes/{id}`
- **Deletar Crime:** `DELETE /crimes/{id}`

### **Batalhas**
- **Simular Batalha:** `POST /battles/criar`
- **Listar Batalhas:** `GET /battles`
- **Detalhes da Batalha:** `GET /battles/{id}`

---

Desenvolvido com inspiração na série *The Boys*. 🌟
