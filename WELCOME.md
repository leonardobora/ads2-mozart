# 🎵 Bem-vindos ao Projeto ADS2 Mozart! 

## 🎯 Visão Geral do Projeto

**Objetivo**: Desenvolver uma rede neural convolucional (CNN) para classificação automática de conteúdo sensível em letras musicais do período 1959-2023.

**Categorias de Classificação**: misoginia, violência, depressão, suicídio, racismo, homofobia

---

## 👥 Divisão da Equipe e Responsabilidades

### 🗂️ **Nathan - Data Steward**
**Papel**: Responsável pelos dados e anotação de conteúdo

**📋 Suas Tarefas:**
1. ✅ **Download e Preparação dos Dados**
   - Executar `python scripts/download_data.py`
   - Validar qualidade dos dados do Kaggle
   - Criar splits treino/validação/teste

2. ✅ **Anotação de Conteúdo Sensível**
   - Rotular 800+ músicas manualmente
   - Seguir critérios de classificação rigorosos
   - Garantir consistência na anotação

3. ✅ **Entrega**
   - `data/processed/train_data.csv` - Dados limpos
   - `data/labeled/songs_labeled_COMPLETE.csv` - Dados anotados
   - Relatório de qualidade dos dados

**📖 Seu Guia**: [`docs/DATA_STEWARD_PT.md`](docs/DATA_STEWARD_PT.md)

---

### 🤖 **Leticia + Leonardo - ML Engineers**
**Papel**: Implementação e treinamento da CNN

**📋 Tarefas da Leticia:**
1. ✅ **Implementação da CNN**
   - Arquitetura do modelo (`src/models/cnn_classifier.py`)
   - Pipeline de preprocessamento (`src/features/text_features.py`)
   - Sistema de métricas customizadas

2. ✅ **Experimentação**
   - Notebook de desenvolvimento (`notebooks/02_model_development.ipynb`)
   - Análise de performance por categoria
   - Otimização de hiperparâmetros

**📋 Tarefas do Leonardo (ML):**
1. ✅ **Pipeline de Treinamento**
   - Script de treinamento (`scripts/train_cnn.py`)
   - Sistema de avaliação (`scripts/evaluate_model.py`)
   - Integração com MLflow/Wandb

2. ✅ **Análise e Validação**
   - Notebook de avaliação (`notebooks/04_model_evaluation.ipynb`)
   - Análise temporal (performance por década)
   - Interpretabilidade do modelo

**📖 Guia Técnico**: [`docs/ML_ENGINEER_PT.md`](docs/ML_ENGINEER_PT.md)

---

### ⚙️ **Leonardo - DevOps Lead**
**Papel**: Infraestrutura, CI/CD e deployment

**📋 Suas Tarefas:**
1. ✅ **GitHub e CI/CD** (CONCLUÍDO)
   - Repositório configurado com GitHub Actions
   - Pipeline de testes automatizados
   - Security scanning implementado

2. ✅ **Containerização** (CONCLUÍDO)
   - Docker setup para dev/prod
   - Docker Compose para stack completa
   - Health checks configurados

3. ✅ **Monitoramento e Deploy**
   - Pipeline de deployment automatizado
   - MLflow para tracking de experimentos
   - Configuração de secrets e variáveis

**📖 Guia Técnico**: [`docs/DEVOPS_PT.md`](docs/DEVOPS_PT.md)

---

### 🧪 **Carlos (QA Lead) + Luan (ML QA) - Testadores**
**Papel**: Garantir qualidade e robustez da solução

**📋 Tarefas do Carlos:**
1. ✅ **Testes de Dados e Sistema**
   - Validação de qualidade dos dados
   - Testes de preprocessamento
   - Testes de containerização Docker
   - Testes de segurança e compliance

2. ✅ **Coordenação de QA**
   - Relatórios de bugs e issues
   - Validação final de entrega
   - Documentação de testes

**📋 Tarefas do Luan:**
1. ✅ **Testes de ML**
   - Validação do treinamento CNN
   - Testes de performance e métricas
   - Testes de reproducibilidade
   - Análise de edge cases

2. ✅ **Testes de API e Inferência**
   - Testes de predição em tempo real
   - Validação de endpoints
   - Performance testing

**📖 Guia de QA**: [`docs/QA_TESTER_PT.md`](docs/QA_TESTER_PT.md)

---

## ⚡ Execução Rápida - 2 Semanas

### **🎯 Prioridades Críticas para Entrega:**
1. **Nathan** → Dados anotados prontos (Semana 1)
2. **Leticia + Leonardo** → CNN funcionando (Semana 1-2)  
3. **Carlos + Luan** → Validação e testes (Semana 2)
4. **Leonardo (DevOps)** → Deploy final (Semana 2)

### **📦 Entregáveis Mínimos Viáveis:**
- ✅ Dataset com 500+ músicas anotadas
- ✅ CNN treinada com F1-score > 0.6
- ✅ Pipeline end-to-end funcionando
- ✅ Documentação básica e demonstração

---

## 📁 Estrutura do Projeto

```
📂 ads2-mozart/
├── 📊 data/                    # Dados (Nathan)
├── 🧠 src/models/             # CNN Implementation (Leticia)
├── 🔧 src/features/           # Preprocessamento (Leonardo ML)
├── 📓 notebooks/              # Análise (Leticia + Leonardo ML)
├── 🚀 scripts/                # Automação (Leonardo ML)
├── 🧪 tests/                  # QA Tests (Carlos + Luan)
├── ⚙️ .github/workflows/      # CI/CD (Leonardo DevOps)
├── 🐳 docker/                 # Containers (Leonardo DevOps)
└── 📚 docs/                   # Documentação (Todos)
```

---

## 🎯 Metas de Qualidade

### **Dados (Nathan)**
- ✅ 500+ músicas anotadas com qualidade (mínimo viável)
- ✅ Confiança média > 3.0/5.0
- ✅ Pelo menos 20 exemplos por categoria

### **Modelo (Leticia + Leonardo ML)**
- ✅ F1-score > 0.6 por categoria
- ✅ ROC-AUC > 0.7 global
- ✅ Sem overfitting significativo

### **Sistema (Leonardo DevOps)**
- ✅ Pipeline CI/CD 100% funcional
- ✅ Deploy automatizado
- ✅ Monitoramento ativo

### **Qualidade (Carlos + Luan)**
- ✅ Coverage de testes > 80%
- ✅ Todos os edge cases testados
- ✅ Performance validada

---

## 🛠️ Primeiros Passos

### **Para Todos:**
1. **Clone o repositório:**
```bash
git clone https://github.com/leonardobora/ads2-mozart.git
cd ads2-mozart
```

2. **Instale dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure ambiente:**
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

### **Iniciar Desenvolvimento:**
- **Nathan**: Siga [`docs/DATA_STEWARD_PT.md`](docs/DATA_STEWARD_PT.md)
- **Leticia/Leonardo**: Siga [`docs/ML_ENGINEER_PT.md`](docs/ML_ENGINEER_PT.md)
- **Carlos/Luan**: Siga [`docs/QA_TESTER_PT.md`](docs/QA_TESTER_PT.md)

---

## 📞 Comunicação

### **Canais de Comunicação:**
- **Issues GitHub**: Para bugs e features
- **Pull Requests**: Para code review
- **Discussions**: Para dúvidas e planejamento

### **Reuniões Sugeridas:**
- **Daily Standup**: 15min diários (opcional)
- **Weekly Review**: Progresso semanal
- **Sprint Planning**: Planejamento de tarefas

---

## 🏆 Objetivos de Entrega

### **Deliverables Finais:**
1. ✅ **Modelo CNN Treinado** - Performance validada
2. ✅ **Dataset Anotado** - 800+ músicas classificadas
3. ✅ **Pipeline Completo** - Do dado bruto à predição
4. ✅ **Documentação Técnica** - Guias e relatórios
5. ✅ **Demonstração** - Sistema funcionando end-to-end

### **Critérios de Sucesso:**
- ✅ Classificação automática de conteúdo sensível
- ✅ Performance superior a baseline simples
- ✅ Sistema robusto e bem testado
- ✅ Código limpo e documentado
- ✅ Pipeline de ML completo e automatizado

---

## 🎉 Vamos Construir Algo Incrível!

**Cada membro tem um papel crucial no sucesso do projeto!**

💪 **Nathan**: Seus dados de qualidade são a base de tudo  
🧠 **Leticia**: Sua CNN será o coração do sistema  
⚡ **Leonardo**: Sua infraestrutura garante que tudo funcione  
🔍 **Carlos/Luan**: Seus testes garantem a excelência

**🚀 Juntos, vamos criar uma solução robusta para classificação de conteúdo musical!**

---

*📝 Para dúvidas específicas, consultem os guias individuais ou abram issues no GitHub.*

**🎵 Let's make some ML magic happen! 🎵**