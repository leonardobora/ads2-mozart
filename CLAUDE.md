# CLAUDE.md

Este arquivo fornece orientações para Claude Code (claude.ai/code) ao trabalhar com código neste repositório.

## Visão Geral do Projeto

Este é um projeto de classificação de conteúdo musical que utiliza CNNs para detectar conteúdo sensível em letras de música (misoginia, violência, depressão, suicídio, racismo, homofobia). O projeto processa dados musicais de 1959-2023 e implementa classificação multi-label.

## Instruções de Desenvolvimento

**IMPORTANTE**: Todo código, comentários, docstrings e documentação devem ser escritos em português brasileiro. Use nomes de variáveis, funções e classes em português quando possível, mantendo clareza e legibilidade.

## Comandos Comuns

### Configuração e Instalação
```bash
pip install -r requirements.txt
pip install -e .  # Instalar pacote em modo desenvolvimento
```

### Operações de Dados
```bash
python scripts/download_data.py              # Baixar dataset do Kaggle
python scripts/data_preprocessing.py         # Processar dados brutos
python scripts/create_labeling_template.py   # Criar templates de rotulação
```

### Treinamento e Avaliação de Modelos
```bash
python scripts/train_model.py --config config/config.yml
python scripts/evaluate_model.py
python scripts/hyperparameter_tuning.py
```

### Testes
```bash
pytest                                       # Executar todos os testes
pytest tests/unit/                          # Executar apenas testes unitários
pytest tests/integration/                   # Executar testes de integração
pytest -m unit                             # Executar testes marcados como unit
pytest -m "not slow"                       # Pular testes lentos
pytest --cov=src                           # Executar com cobertura
```

### Qualidade do Código
```bash
black src/ tests/ scripts/                  # Formatar código
flake8 src/ tests/ scripts/                 # Verificar código
```

## Arquitetura

### Pipeline de Dados
- Dados musicais brutos do Kaggle → `data/raw/`
- Pré-processamento → `data/processed/` 
- Rotulação manual → `data/labeled/`
- Divisões treino/validação/teste gerenciadas por `src/data/splitter.py`

### Arquitetura do Modelo
- Classificação multi-label baseada em CNN
- Embeddings: 300 dimensões
- Convoluções: filtros n-gram 2,3,4,5 (128 cada)
- 6 categorias de conteúdo sensível + 1 categoria limpa
- Configuração baseada em `config/config.yml`

### Componentes Principais
- `src/models/base_model.py` - Classe base abstrata para todos os modelos
- `src/models/cnn_models.py` - Implementações CNN
- `src/features/text_features.py` - Pré-processamento de texto e extração de features
- `src/data/data_loader.py` - Utilitários de carregamento de dados
- `src/utils/metrics.py` - Métricas customizadas para classificação multi-label

### Configuração
- Config principal: `config/config.yml` (dados, modelo, parâmetros de treinamento)
- Configs específicos de modelo: `config/model_configs.yml`
- Todas as configurações são baseadas em YAML e específicas do ambiente

### Rastreamento de Experimentos
- Integração MLflow e Weights & Biases
- Checkpoints de modelos salvos em `models/checkpoints/`
- Resultados e relatórios em `results/`

## Notas de Desenvolvimento

### Estrutura da Equipe
- Data Steward: Preparação e anotação de dados
- Engenheiros ML: Implementação e treinamento de modelos  
- DevOps: Infraestrutura e deployment
- QA: Testes e validação

### Manipulação de Dados
- Classificação de conteúdo sensível requer cuidado especial com dados
- Rótulos: misoginia, violência, depressão, suicídio, racismo, homofobia, limpo
- Classificação multi-label (músicas podem ter múltiplas categorias)
- Sequências de texto limitadas a máximo 512 tokens

### Estratégia de Testes
- Testes unitários para componentes individuais
- Testes de integração para pipeline completo
- Testes de performance para inferência do modelo
- Testes de segurança para manipulação de dados

## Checklist de Progresso do Projeto

### 📊 Fase 1: Preparação de Dados (Data Steward - Nathan)
- [ ] Download e validação do dataset Kaggle
- [ ] Limpeza e pré-processamento dos dados brutos
- [ ] Criação de templates de rotulação
- [ ] Anotação manual de 800+ músicas
- [ ] Validação da qualidade das anotações
- [ ] Criação dos conjuntos treino/validação/teste
- [ ] Documentação do processo de anotação

### 🤖 Fase 2: Desenvolvimento ML (Leticia + Leonardo)
- [ ] Implementação da arquitetura CNN base
- [ ] Desenvolvimento do pipeline de pré-processamento de texto
- [ ] Implementação de métricas customizadas
- [ ] Sistema de embeddings e features temporais
- [ ] Pipeline de treinamento automatizado
- [ ] Sistema de avaliação e validação
- [ ] Notebooks de experimentação e análise
- [ ] Otimização de hiperparâmetros
- [ ] Análise de interpretabilidade do modelo

### ⚙️ Fase 3: Infraestrutura (Leonardo - DevOps)
- [ ] Configuração do ambiente Docker
- [ ] Pipeline CI/CD com GitHub Actions
- [ ] Integração MLflow/Weights & Biases
- [ ] Automação de testes
- [ ] Deploy automatizado
- [ ] Monitoramento e logging
- [ ] Configuração de secrets e variáveis
- [ ] Documentação de deployment

### 🧪 Fase 4: Qualidade e Testes (Carlos + Luan)
- [ ] Testes unitários para todos os componentes
- [ ] Testes de integração do pipeline completo
- [ ] Testes de performance e escalabilidade
- [ ] Testes de segurança e compliance
- [ ] Validação de reprodutibilidade
- [ ] Testes de edge cases e robustez
- [ ] Documentação de testes
- [ ] Relatório final de qualidade

### 📈 Metas de Performance
- [ ] F1-score > 0.6 por categoria
- [ ] ROC-AUC > 0.7 global
- [ ] Tempo de inferência < 100ms por música
- [ ] Cobertura de testes > 80%
- [ ] Zero vazamentos de dados sensíveis

### 📚 Entregáveis Finais
- [ ] Modelo CNN treinado e validado
- [ ] Dataset completo com 800+ músicas anotadas
- [ ] Pipeline end-to-end funcional
- [ ] Documentação técnica completa
- [ ] Demonstração do sistema
- [ ] Relatório de resultados e análises