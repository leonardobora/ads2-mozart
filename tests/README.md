# 🧪 Guia de Execução de Testes - ADS2 Mozart

## Estrutura de Testes

```
tests/
├── unit/                  # Testes unitários (Carlos)
│   ├── test_data_loader.py
│   ├── test_preprocessor.py
│   ├── test_cnn_model.py
│   └── test_utils.py
├── integration/           # Testes de integração (Luan)
│   ├── test_data_pipeline.py
│   ├── test_ml_pipeline.py
│   └── test_api_endpoints.py
├── performance/           # Testes de performance (Luan)
│   ├── test_training_speed.py
│   ├── test_inference_speed.py
│   └── test_memory_usage.py
├── security/              # Testes de segurança (Carlos)
│   ├── test_data_privacy.py
│   ├── test_input_validation.py
│   └── test_secrets_exposure.py
└── fixtures/              # Dados de teste
    ├── sample_data.csv
    └── mock_responses.json
```

## Como Executar os Testes

### Testes Unitários
```bash
# Todos os testes unitários
pytest tests/unit/ -v

# Teste específico
pytest tests/unit/test_data_loader.py -v

# Com coverage
pytest tests/unit/ --cov=src --cov-report=html
```

### Testes de Integração
```bash
# Todos os testes de integração
pytest tests/integration/ -v

# Apenas pipeline de dados
pytest tests/integration/test_data_pipeline.py -v
```

### Testes de Performance
```bash
# Benchmarks de performance
pytest tests/performance/ --benchmark-only

# Com relatório detalhado
pytest tests/performance/ --benchmark-sort=mean --benchmark-save=results
```

### Testes de Segurança
```bash
# Testes de segurança
pytest tests/security/ -v

# Com relatório de vulnerabilidades
pytest tests/security/ --security-report
```

## Configuração do Ambiente de Teste

### Dependências Adicionais
```bash
pip install pytest pytest-cov pytest-benchmark pytest-mock
pip install factory-boy faker  # Para dados de teste
```

### Variáveis de Ambiente
```bash
export TEST_ENV=true
export TEST_DATA_PATH=tests/fixtures/
export KAGGLE_USERNAME=test_user
export KAGGLE_KEY=test_key
```

## Relatórios de Teste

### Coverage Report
```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
open htmlcov/index.html  # Ver relatório visual
```

### Benchmark Report
```bash
pytest tests/performance/ --benchmark-save=baseline
pytest tests/performance/ --benchmark-compare=baseline
```

## Automatização

### Pre-commit Hooks
```bash
# Instalar pre-commit
pip install pre-commit
pre-commit install

# Executar manualmente
pre-commit run --all-files
```

### GitHub Actions
Os testes são executados automaticamente em:
- Push para main/develop
- Pull requests
- Releases

## Casos de Teste Prioritários

### 🔴 Críticos (devem sempre passar)
- Carregamento de dados sem erros
- Treinamento do modelo sem crash
- Predições retornam formato correto
- API responde com status 200

### 🟡 Importantes (podem falhar ocasionalmente)
- Performance dentro dos limites
- Memory usage otimizado
- Tempo de resposta aceitável

### 🟢 Opcionais (nice to have)
- Edge cases específicos
- Testes de stress
- Compatibilidade entre versões