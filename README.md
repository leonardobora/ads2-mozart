# ADS2 Mozart - Music Content Classification with CNN

🎵 **Classificação de Conteúdo Sensível em Letras Musicais usando Redes Neurais Convolucionais**

## Visão Geral

Este projeto implementa uma rede neural convolucional (CNN) para classificar conteúdo sensível em letras musicais populares do período de 1959-2023. O sistema identifica automaticamente categorias como misoginia, violência, depressão, suicídio, racismo e homofobia.

## Estrutura do Projeto

```
├── data/                   # Dados (gitignored por segurança)
├── src/                    # Código fonte
│   ├── data/              # Processamento de dados
│   ├── models/            # Arquitetura CNN
│   ├── features/          # Feature engineering
│   └── utils/             # Utilitários
├── notebooks/             # Análise e experimentação
├── config/                # Configurações
├── scripts/               # Scripts de automação
├── docs/                  # Documentação do projeto
└── .github/               # CI/CD com GitHub Actions
```

## Quick Start

### 1. Instalação
```bash
git clone https://github.com/leonardobora/ads2-mozart.git
cd ads2-mozart
pip install -r requirements.txt
```

### 2. Download dos Dados
```bash
python scripts/download_data.py
```

### 3. Treinamento da CNN
```bash
python scripts/train_cnn.py --config config/config.yml
```

## Papéis da Equipe

- **🗂️ Data Steward**: Preparação e anotação de dados ([Guia](docs/DATA_STEWARD_PT.md))
- **🤖 ML Engineer**: Implementação e treinamento da CNN ([Guia](docs/ML_ENGINEER_PT.md))
- **⚙️ DevOps**: Infraestrutura e CI/CD ([Guia](docs/DEVOPS_PT.md))

## Tecnologias

- **ML Framework**: PyTorch
- **Data**: Kaggle Dataset (1959-2019)
- **Deployment**: Docker + GitHub Actions
- **Monitoring**: MLflow / Weights & Biases

## Dataset

Utilizamos o dataset "Top 100 Songs and Lyrics from 1959 to 2019" do Kaggle, com anotações manuais para 6 categorias de conteúdo sensível.

## Arquitetura CNN

- **Embedding**: 300 dimensões
- **Convoluções**: Filtros de 2, 3, 4, 5 n-gramas
- **Classificação**: Multi-label (6 categorias)
- **Regularização**: Dropout + Weight Decay

## Contribuição

1. Fork o projeto
2. Crie uma feature branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto é para fins acadêmicos e de pesquisa.

---

**🎓 Projeto ADS2 - Análise de Dados e Sistemas 2**