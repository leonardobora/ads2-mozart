# 🤖 Guia do ML Engineer - Projeto Mozart CNN

## Visão Geral
Como **ML Engineer** do projeto, você é responsável por implementar, treinar e otimizar a rede neural convolucional (CNN) para classificação de conteúdo sensível em letras musicais.

---

## 🎯 Suas Responsabilidades

### 1. **Arquitetura da CNN**
- Implementar modelo CNN otimizado para classificação de texto
- Definir camadas de embedding, convolução e pooling
- Configurar arquitetura multi-label para 6 categorias sensíveis

### 2. **Pipeline de Treinamento**
- Configurar processo de treinamento com validação
- Implementar early stopping e checkpointing
- Monitorar métricas de performance

### 3. **Otimização e Avaliação**
- Tuning de hiperparâmetros
- Validação cruzada temporal
- Análise de performance por categoria

### 4. **Deploy e Monitoramento**
- Preparar modelo para produção
- Implementar pipeline de inferência
- Configurar monitoramento de drift

---

## 🚀 Roadmap - Implementação da CNN

### **FASE 1: Preparação do Ambiente**

**🔧 Dependências Técnicas:**
- Aguardar dados rotulados do Data Steward
- Verificar configuração GPU/CPU
- Instalar dependências ML

**📋 Checklist Pré-Requisitos:**
- [ ] Arquivo `data/labeled/songs_labeled_COMPLETE.csv` disponível
- [ ] Pelo menos 800 músicas anotadas
- [ ] Python 3.8+ com torch instalado
- [ ] Acesso a GPU (recomendado)

### **FASE 2: Análise dos Dados Rotulados**

**🎯 Objetivos:**
- Entender distribuição dos rótulos
- Identificar desbalanceamento de classes
- Definir estratégia de balanceamento

**🔍 Análises Necessárias:**
- Distribuição por categoria (misogyny, violence, etc.)
- Correlação entre categorias
- Análise temporal dos rótulos
- Comprimento médio das letras por categoria

**📊 Métricas Esperadas:**
- Pelo menos 50 exemplos positivos por categoria
- Distribuição não muito desbalanceada (< 10:1)
- Correlação moderada entre categorias (< 0.7)

### **FASE 3: Preprocessamento para CNN**

**🛠️ Tarefas de Preprocessamento:**

1. **Tokenização e Vocabulário:**
   - Criar vocabulário com 10k palavras mais frequentes
   - Implementar padding para sequências de 512 tokens
   - Adicionar tokens especiais (UNK, PAD)

2. **Encoding dos Labels:**
   - Multi-hot encoding para 6 categorias
   - Estratégia para exemplos sem rótulos positivos
   - Pesos de classe para balanceamento

3. **Divisão Temporal:**
   - Split por década (não aleatório)
   - Treino: 1959-2009, Teste: 2010-2019
   - Validação: 20% do treino (aleatório)

### **FASE 4: Arquitetura CNN**

**🏗️ Componentes da Rede:**

1. **Embedding Layer:**
   - Dimensão: 300 (configurável)
   - Pré-treinado: Word2Vec ou GloVe opcional
   - Trainable: True

2. **Convolutional Layers:**
   - Filtros: [2, 3, 4, 5] n-gramas
   - Número de filtros: 128 por tamanho
   - Ativação: ReLU
   - Dropout: 0.5

3. **Pooling e Classification:**
   - Global Max Pooling para cada filtro
   - Concatenação dos features
   - Dense layer: 256 → 6 (sigmoid)

**⚙️ Configurações Técnicas:**
- Loss: Binary Cross Entropy (multi-label)
- Optimizer: Adam (lr=0.001)
- Metrics: F1-score, Precision, Recall por categoria
- Regularização: Dropout + Weight Decay

### **FASE 5: Treinamento e Validação**

**🎯 Estratégia de Treinamento:**

1. **Configuração Base:**
   - Batch size: 32
   - Epochs: 50 (com early stopping)
   - Patience: 10 epochs
   - Salvar melhor modelo por F1-score

2. **Técnicas de Regularização:**
   - Dropout nas camadas densas
   - Weight decay (L2): 0.01
   - Learning rate scheduling (ReduceLROnPlateau)

3. **Validação:**
   - Validação por época
   - Métricas por categoria individual
   - Matriz de confusão por categoria
   - Análise de casos difíceis

### **FASE 6: Otimização de Hiperparâmetros**

**🔬 Experimentos Planejados:**

1. **Grid Search Básico:**
   - Learning rate: [0.01, 0.001, 0.0001]
   - Dropout: [0.3, 0.5, 0.7]
   - Filtros por tamanho: [64, 128, 256]

2. **Arquitetura:**
   - Dimensão embedding: [200, 300, 400]
   - Filtros: [2,3,4], [3,4,5], [2,3,4,5]
   - Pooling: Max vs Average

3. **Dados:**
   - Balanceamento: undersampling vs oversampling
   - Sequence length: [256, 512, 1024]
   - Vocabulário: [5k, 10k, 20k]

### **FASE 7: Avaliação Profunda**

**📈 Métricas de Avaliação:**

1. **Métricas Gerais:**
   - F1-score macro e micro
   - Precision/Recall por categoria
   - ROC-AUC para cada categoria
   - Hamming Loss (multi-label)

2. **Análises Específicas:**
   - Performance por década
   - Análise de confusão entre categorias
   - Casos de falsos positivos/negativos
   - Interpretabilidade (attention maps)

3. **Validação Temporal:**
   - Performance em dados de décadas não vistas
   - Degradação temporal do modelo
   - Bias por época musical

### **FASE 8: Preparação para Produção**

**🚀 Deploy Pipeline:**

1. **Otimização do Modelo:**
   - Quantização (opcional)
   - ONNX export para compatibilidade
   - Benchmark de inferência

2. **API de Predição:**
   - Interface REST para predições
   - Batch processing para múltiplas músicas
   - Validação de input

3. **Monitoramento:**
   - Drift detection nos inputs
   - Performance monitoring
   - Logging de predições

---

## 📋 Checklist Técnico - ML Engineer

### **Preparação** ✅
- [ ] Dados rotulados recebidos do Data Steward
- [ ] Ambiente de desenvolvimento configurado
- [ ] GPU disponível e testada
- [ ] Dependências instaladas

### **Implementação** ✅
- [ ] Módulo de preprocessamento implementado
- [ ] Arquitetura CNN implementada
- [ ] Pipeline de treinamento funcional
- [ ] Sistema de métricas configurado

### **Experimentação** ✅
- [ ] Baseline CNN treinado
- [ ] Hiperparâmetros otimizados
- [ ] Validação temporal executada
- [ ] Relatório de performance gerado

### **Produção** ✅
- [ ] Modelo final selecionado
- [ ] Pipeline de inferência testado
- [ ] API de predição implementada
- [ ] Monitoramento configurado

---

## 🛠️ Arquivos a Implementar

### **Módulos Python:**
1. `src/models/cnn_classifier.py` - Arquitetura CNN
2. `src/models/trainer.py` - Loop de treinamento
3. `src/models/evaluator.py` - Métricas e avaliação
4. `src/features/text_features.py` - Preprocessamento
5. `src/utils/metrics.py` - Métricas customizadas

### **Scripts de Execução:**
1. `scripts/train_cnn.py` - Script de treinamento
2. `scripts/evaluate_model.py` - Avaliação do modelo
3. `scripts/hyperparameter_tuning.py` - Otimização
4. `scripts/export_model.py` - Export para produção

### **Notebooks de Análise:**
1. `notebooks/02_model_development.ipynb` - Desenvolvimento
2. `notebooks/03_hyperparameter_tuning.ipynb` - Tuning
3. `notebooks/04_model_evaluation.ipynb` - Avaliação
4. `notebooks/05_error_analysis.ipynb` - Análise de erros

---

## 🚨 Dependências e Limitações

### **Dependências Críticas:**
- **Data Steward**: Dados rotulados de qualidade
- **DevOps**: Infraestrutura de treinamento
- **Hardware**: GPU recomendada para treinamento

### **Limitações Técnicas:**
- Dataset relativamente pequeno (800-1000 músicas)
- Multi-label classification (mais complexo)
- Possível desbalanceamento de classes
- Temporal drift entre décadas

### **Riscos e Mitigações:**
- **Overfitting**: Usar dropout e validação rigorosa
- **Bias temporal**: Validação por década
- **Classes raras**: Técnicas de balanceamento
- **Interpretabilidade**: Implementar attention/saliency

---

## 📞 Comunicação com Equipe

### **Com Data Steward:**
- **Receber**: Dados rotulados, estatísticas de qualidade
- **Validar**: Distribuição dos rótulos, consistência
- **Feedback**: Problemas encontrados nos dados

### **Com DevOps:**
- **Especificar**: Requisitos de hardware/software
- **Integrar**: Pipeline de treinamento automatizado
- **Monitorar**: Métricas de modelo em produção

### **Com Supervisor:**
- **Reportar**: Progress dos experimentos
- **Discutir**: Decisões de arquitetura
- **Apresentar**: Resultados e limitações

---

## 📚 Recursos Técnicos

### **Documentação:**
- `config/config.yml` - Configurações do modelo
- `docs/model_architecture.md` - Detalhes técnicos
- `results/experiments/` - Logs de experimentos

### **Referências:**
- Kim, Y. (2014) - "Convolutional Neural Networks for Sentence Classification"
- Zhang, X. (2015) - "Character-level CNNs for Text Classification"
- Papers sobre multi-label text classification

**✅ Você está pronto para implementar uma CNN robusta para classificação de conteúdo musical sensível!**