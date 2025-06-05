# 🧪 Guia dos Testadores - Projeto Mozart CNN

## Visão Geral
Como **QA Testers** do projeto (Carlos e Luan), vocês são responsáveis por garantir a qualidade, confiabilidade e robustez da solução de classificação de conteúdo musical usando CNN.

---

## 🎯 Suas Responsabilidades

### 1. **Testes de Dados e Pipeline**
- Validar qualidade dos dados processados
- Testar pipeline de preprocessamento
- Verificar integridade dos datasets
- Validar splits de treino/teste/validação

### 2. **Testes do Modelo CNN**
- Testar treinamento da rede neural
- Validar métricas de performance
- Verificar reproducibilidade dos resultados
- Testar inferência em novos dados

### 3. **Testes de Sistema e API**
- Testar endpoints de predição
- Validar containerização (Docker)
- Verificar deployment e rollback
- Testar monitoramento e logs

### 4. **Testes de Segurança e Compliance**
- Verificar handling de dados sensíveis
- Testar proteção de secrets/APIs
- Validar compliance com requisitos
- Testar backup e recovery

---

## 🚀 Plano de Testes - Fases

### **FASE 1: Testes de Dados (Carlos)**

**🔍 Testes de Qualidade dos Dados:**

1. **Download e Carregamento:**
```bash
# Teste básico de download
python scripts/download_data.py
python scripts/validate_data.py --verbose
```

**📋 Checklist de Validação:**
- [ ] Dataset baixado com sucesso do Kaggle
- [ ] Estrutura de dados conforme especificação
- [ ] Encoding UTF-8 correto
- [ ] Sem dados corrompidos ou vazios
- [ ] Distribuição temporal (1959-2019) válida

2. **Preprocessamento:**
```python
# Teste de preprocessamento
from src.data.preprocessor import TextPreprocessor
preprocessor = TextPreprocessor()
# Validar tokenização, limpeza, normalização
```

**🎯 Testes Específicos:**
- Tokenização preserva contexto importante
- Limpeza não remove informação relevante
- Normalização é consistente
- Handling de caracteres especiais

3. **Anotação e Labels:**
```python
# Validar dados anotados
import pandas as pd
df = pd.read_csv('data/labeled/songs_labeled_COMPLETE.csv')
# Verificar consistência, distribuição, qualidade
```

**📊 Métricas de Qualidade:**
- Pelo menos 800 músicas anotadas
- Distribuição balanceada entre categorias
- Consistência inter-anotador > 80%
- Confiança média > 3.0/5.0

### **FASE 2: Testes de ML Pipeline (Luan)**

**🤖 Testes do Modelo CNN:**

1. **Treinamento e Convergência:**
```bash
# Teste de treinamento básico
python scripts/train_cnn.py --config config/test_config.yml --epochs 5
```

**🔬 Validações de Treinamento:**
- [ ] Modelo converge sem erros
- [ ] Loss diminui ao longo das épocas
- [ ] Métricas de validação são consistentes
- [ ] Checkpoints são salvos corretamente
- [ ] Early stopping funciona adequadamente

2. **Performance e Métricas:**
```python
# Teste de avaliação
python scripts/evaluate_model.py --model models/test_model.pt
```

**📈 Métricas Esperadas:**
- F1-score > 0.6 para cada categoria
- Precision/Recall balanceados
- ROC-AUC > 0.7 por categoria
- Sem overfitting significativo

3. **Inferência e Predição:**
```python
# Teste de predição em novos dados
from src.models.cnn_classifier import CNNClassifier
model = CNNClassifier.load('models/trained/best_model.pt')
predictions = model.predict(['test lyrics here'])
```

**🎯 Testes de Robustez:**
- Predições consistentes para inputs similares
- Handling de textos muito curtos/longos
- Performance em diferentes décadas
- Detecção de casos edge

### **FASE 3: Testes de Sistema (Carlos + Luan)**

**🐳 Testes de Containerização:**

1. **Docker Build e Run:**
```bash
# Teste de build
docker build -t ads2-mozart-test .
docker run --rm ads2-mozart-test

# Teste com docker-compose
docker-compose up -d mozart-dev
docker-compose exec mozart-dev python -c "import src; print('OK')"
```

2. **API e Endpoints (quando implementados):**
```bash
# Teste de API
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"lyrics": "test song lyrics"}'
```

**⚡ Testes de Performance:**
- Tempo de resposta < 2 segundos
- Throughput mínimo: 10 predições/segundo
- Memory usage estável
- CPU usage otimizado

### **FASE 4: Testes de Integração**

**🔄 CI/CD Pipeline:**

1. **GitHub Actions:**
```bash
# Triggear workflows manualmente
# Verificar se todos os checks passam
# Validar artifacts gerados
```

**📋 Validação de Workflows:**
- [ ] CI passa em todas as branches
- [ ] Tests automatizados executam
- [ ] Build Docker funciona
- [ ] Deploy pipeline é executado
- [ ] Security scans passam

2. **MLflow e Experiment Tracking:**
```python
# Verificar tracking de experimentos
import mlflow
# Validar logs, métricas, modelos
```

---

## 📋 Checklist Completo de Testes

### **Dados e Preprocessamento** ✅
- [ ] Download automático funciona
- [ ] Validação de dados implementada
- [ ] Preprocessamento preserva qualidade
- [ ] Splits são estratificados corretamente
- [ ] Anotações têm qualidade suficiente

### **Modelo e Treinamento** ✅
- [ ] CNN treina sem erros
- [ ] Métricas atingem baseline esperado
- [ ] Modelo não apresenta overfitting
- [ ] Inferência é rápida e precisa
- [ ] Reproducibilidade garantida

### **Sistema e Deployment** ✅
- [ ] Docker containers funcionam
- [ ] API responde corretamente
- [ ] Monitoramento está ativo
- [ ] Logs são gerados adequadamente
- [ ] Backup/recovery testados

### **Segurança e Compliance** ✅
- [ ] Secrets não expostos em código
- [ ] Dados sensíveis protegidos
- [ ] Scans de segurança passam
- [ ] Compliance com requisitos acadêmicos
- [ ] Documentation está completa

---

## 🛠️ Ferramentas de Teste

### **Automação de Testes:**
```python
# pytest para unit tests
pytest tests/ -v --cov=src

# Testes de integração
pytest tests/integration/ -v

# Testes de performance
pytest tests/performance/ -v --benchmark
```

### **Testes Manuais:**
- **Jupyter Notebooks**: Para análise exploratória
- **Docker**: Para testes de containerização
- **Postman/curl**: Para testes de API
- **Browser**: Para interfaces web (se implementadas)

### **Monitoramento:**
```bash
# Health checks
docker exec mozart-prod python -c "import src; print('Health OK')"

# Logs
docker-compose logs -f mozart-prod

# Métricas
curl http://localhost:9090/metrics
```

---

## 🚨 Cenários de Teste Críticos

### **Edge Cases para Testar:**

1. **Dados Problemáticos:**
   - Letras muito curtas (< 10 palavras)
   - Letras muito longas (> 1000 palavras)
   - Caracteres especiais e emojis
   - Textos em idiomas diferentes

2. **Falhas de Sistema:**
   - Perda de conexão durante download
   - Corrupção de modelo durante salvamento
   - Falta de memória durante treinamento
   - Timeout em predições

3. **Cenários de Segurança:**
   - Injection attacks em inputs
   - Acesso não autorizado à API
   - Exposição de dados sensíveis
   - Tentativas de bypass de validação

---

## 📞 Comunicação e Relatórios

### **Divisão de Responsabilidades:**

**Carlos (QA Lead):**
- Coordenação geral dos testes
- Testes de dados e qualidade
- Relatórios de bugs e issues
- Validação final de entrega

**Luan (ML QA):**
- Testes específicos do modelo CNN
- Performance e métricas
- Testes de reprodutibilidade
- Análise de resultados

### **Comunicação com Equipe:**

**Com Data Steward (Nathan):**
- **Validar**: Qualidade dos dados processados
- **Reportar**: Problemas encontrados nos dados
- **Coordenar**: Re-anotação se necessário

**Com ML Engineers (Leticia + Leonardo):**
- **Testar**: Implementações de modelo
- **Validar**: Performance e métricas
- **Reportar**: Bugs e problemas de treinamento

**Com DevOps (Leonardo):**
- **Validar**: Pipelines de CI/CD
- **Testar**: Deployment e infraestrutura
- **Coordenar**: Fixes de ambiente

### **Relatórios de Teste:**
```
📊 Relatório Semanal de QA:
- Testes executados: X
- Bugs encontrados: Y  
- Bugs resolvidos: Z
- Coverage de código: W%
- Métricas de modelo: [lista]
- Status geral: ✅/⚠️/❌
```

---

## 📚 Recursos e Documentação

### **Documentação Técnica:**
- `tests/README.md` - Guia de execução de testes
- `docs/test_cases.md` - Casos de teste detalhados
- `docs/bug_reports.md` - Template de relatório de bugs

### **Scripts de Teste:**
- `tests/test_data_quality.py` - Testes de dados
- `tests/test_model_performance.py` - Testes de modelo
- `tests/test_api_endpoints.py` - Testes de API
- `tests/test_security.py` - Testes de segurança

**✅ Garantir qualidade excepcional do projeto Mozart CNN!**