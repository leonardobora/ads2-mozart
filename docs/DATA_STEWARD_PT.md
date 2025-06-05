# 📊 Guia do Data Steward - Projeto Mozart

## Visão Geral
Como **Data Steward** do projeto de classificação de conteúdo sensível em letras musicais, você é responsável pela gestão, qualidade e preparação dos dados que alimentarão nossa rede neural CNN.

---

## 🎯 Suas Responsabilidades

### 1. **Coleta e Aquisição de Dados**
- Baixar e validar datasets de letras musicais
- Garantir integridade dos dados brutos
- Documentar proveniência dos dados

### 2. **Qualidade e Limpeza**
- Identificar e corrigir inconsistências
- Remover duplicatas e dados corrompidos
- Validar formatos e estruturas

### 3. **Anotação de Conteúdo Sensível**
- Rotular manualmente conteúdo problemático
- Classificar: misoginia, violência, depressão, suicídio, racismo, homofobia
- Garantir consistência na anotação
- Documentar critérios utilizados

### 4. **Preparação para ML**
- Criar splits treino/validação/teste
- Normalizar formatos de texto
- Gerar datasets rotulados prontos para a CNN

---

## 🚀 Passo a Passo - Preparação dos Dados

### **ETAPA 1: Configuração do Ambiente**

```bash
# 1. Clone o repositório (se necessário)
cd /home/leonardobora/mozart_aps2

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Verifique se o ambiente está funcionando
python -c "import pandas as pd; import numpy as np; print('✅ Ambiente OK')"
```

### **ETAPA 2: Download dos Dados**

```bash
# Execute o script de download
python scripts/download_data.py

# Verifique se os dados foram baixados
ls -la data/raw/
```

**❗ O que verificar:**
- Arquivo CSV foi criado em `data/raw/`
- Não há erros de conexão ou autenticação
- Dataset contém as colunas esperadas: title, artist, year, lyrics

### **ETAPA 3: Exploração Inicial dos Dados**

```bash
# Execute o notebook de exploração
jupyter notebook notebooks/01_data_exploration.ipynb
```

**📋 Checklist de Validação:**
- [ ] Dataset tem entre 5.000-10.000 músicas
- [ ] Período temporal: 1959-2019
- [ ] Letras em inglês e português
- [ ] Sem campos vazios críticos
- [ ] Distribuição temporal equilibrada

### **ETAPA 4: Análise de Qualidade dos Dados**

```python
# Execute este código para análise detalhada
from src.data.data_loader import MusicDataLoader

loader = MusicDataLoader()
df = loader.load_local_csv('data/raw/kaggle_brianblakely_top-100-songs-and-lyrics-from-1959-to-2019.csv')

# Verifique a qualidade
is_valid, issues = loader.validate_dataset(df)
print(f"Dataset válido: {is_valid}")
if issues:
    print("Problemas encontrados:", issues)
```

### **ETAPA 5: Pré-processamento de Texto**

```bash
# Execute o script de pré-processamento
python scripts/data_preprocessing.py --input data/raw/ --output data/processed/
```

**🔧 O que este script faz:**
- Remove caracteres especiais desnecessários
- Normaliza encodings (UTF-8)
- Padroniza formatos de data/ano
- Remove duplicatas exatas
- Cria colunas derivadas (word_count, char_count)

### **ETAPA 6: Criação dos Splits de Dados**

```python
# Execute para criar divisões treino/teste
from src.data.splitter import create_stratified_split

# Carregue os dados processados
df = pd.read_csv('data/processed/music_lyrics_cleaned.csv')

# Crie os splits
train_df, val_df, test_df = create_stratified_split(
    df, 
    test_size=0.2, 
    val_size=0.1,
    stratify_by='decade'  # Equilibra por década
)

# Salve os splits
train_df.to_csv('data/processed/train_data.csv', index=False)
val_df.to_csv('data/processed/val_data.csv', index=False)
test_df.to_csv('data/processed/test_data.csv', index=False)
```

### **ETAPA 7: Preparação para Rotulação**

```bash
# Crie arquivo para rotulação manual
python scripts/create_labeling_template.py --sample 1000 --output data/labeled/
```

**📝 Arquivo de rotulação criado:**
- `data/labeled/songs_to_label.csv`
- Contém 1000 músicas selecionadas aleatoriamente
- Colunas para rotular: misogyny, violence, depression, suicide, racism, homophobia

### **ETAPA 8: Anotação Manual de Conteúdo Sensível**

**🎯 Processo de Anotação:**

1. **Abra o arquivo de rotulação:**
```bash
# Use Excel, LibreOffice ou editor de sua preferência
libreoffice data/labeled/songs_to_label.csv
```

2. **Leia as instruções completas:**
```bash
cat data/labeled/INSTRUCTIONS_PT.md
```

3. **Para cada música, analise a coluna `lyrics_preview` e preencha:**
   - **misogyny**: 0 ou 1
   - **violence**: 0 ou 1  
   - **depression**: 0 ou 1
   - **suicide**: 0 ou 1
   - **racism**: 0 ou 1
   - **homophobia**: 0 ou 1
   - **annotator_id**: Seu nome/iniciais
   - **confidence**: 1-5 (nível de certeza)

4. **Critérios de Qualidade:**
   - ✅ Rotule pelo menos 800 músicas (de 1000)
   - ✅ Mantenha consistência nos critérios
   - ✅ Use confidence baixa quando incerto
   - ✅ Adicione notas em casos especiais

5. **Salve o arquivo anotado:**
```bash
# Salve como: data/labeled/songs_labeled_COMPLETE.csv
```

### **ETAPA 9: Validação da Anotação**

```python
# Execute para validar sua anotação
import pandas as pd

# Carregue dados anotados
df_labeled = pd.read_csv('data/labeled/songs_labeled_COMPLETE.csv')

# Estatísticas da anotação
labels = ['misogyny', 'violence', 'depression', 'suicide', 'racism', 'homophobia']
print("📊 Estatísticas da Anotação:")
for label in labels:
    if label in df_labeled.columns:
        count = df_labeled[label].sum()
        total = df_labeled[label].notna().sum()
        print(f"   {label}: {count}/{total} ({count/total*100:.1f}%)")

# Verificar qualidade
missing_annotations = df_labeled[labels].isnull().sum().sum()
print(f"\n⚠️ Anotações faltando: {missing_annotations}")

# Confiança média
if 'confidence' in df_labeled.columns:
    avg_confidence = df_labeled['confidence'].mean()
    print(f"🎯 Confiança média: {avg_confidence:.1f}/5")
```

---

## 📋 Checklist Final - Data Steward

### **Dados Brutos** ✅
- [ ] Dataset baixado com sucesso
- [ ] Proveniência documentada
- [ ] Backup criado em local seguro
- [ ] Metadados registrados

### **Qualidade dos Dados** ✅
- [ ] Validação automática passou
- [ ] Duplicatas removidas
- [ ] Campos obrigatórios preenchidos
- [ ] Encoding padronizado (UTF-8)
- [ ] Distribuição temporal verificada

### **Dados Processados** ✅
- [ ] Splits criados (70% treino, 20% teste, 10% validação)
- [ ] Estratificação por década aplicada
- [ ] Arquivo de rotulação preparado
- [ ] Documentação atualizada

### **Anotação de Conteúdo** ✅
- [ ] Pelo menos 800 músicas anotadas
- [ ] Critérios de classificação documentados
- [ ] Confiança média > 3.0
- [ ] Arquivo `songs_labeled_COMPLETE.csv` salvo
- [ ] Validação estatística executada

### **Preparação para CNN** ✅
- [ ] Formato compatível com pipeline ML
- [ ] Dados rotulados prontos para treinamento
- [ ] Vocabulário extraído
- [ ] Features numéricas normalizadas

---

## 🚨 Problemas Comuns e Soluções

### **Erro: "kagglehub not found"**
```bash
pip install kagglehub[pandas-datasets]
```

### **Erro: "Dataset muito pequeno"**
- Verifique conexão com internet
- Confirme nome do dataset Kaggle
- Tente download manual

### **Erro: "Encoding problems"**
```python
# Force UTF-8 encoding
df = pd.read_csv('file.csv', encoding='utf-8', errors='ignore')
```

### **Erro: "Duplicatas não removidas"**
```python
# Remove duplicatas manuais
df = df.drop_duplicates(subset=['title', 'artist'], keep='first')
```

---

## 📞 Próximos Passos

Após completar estas etapas, entregue para a equipe:

1. **Arquivo `data/processed/train_data.csv`** - Dados de treino limpos
2. **Arquivo `data/processed/test_data.csv`** - Dados de teste  
3. **Arquivo `data/labeled/songs_labeled_COMPLETE.csv`** - Dados anotados para treinamento
4. **Relatório de qualidade** - Salvem `logs/data_quality_report.txt`
5. **Estatísticas de anotação** - Distribuição dos rótulos

**🔄 Contato com outros membros:**
- **ML Engineer**: Entregar dados rotulados prontos para CNN
- **DevOps**: Verificar pipelines de dados
- **Supervisor**: Relatório de qualidade da anotação

---

## 📚 Recursos Adicionais

- **Documentação técnica**: `docs/data_format.md`
- **Scripts úteis**: `scripts/`
- **Configurações**: `config/config.yml`
- **Logs**: `logs/`

**✅ Sucesso!** Seus dados estão prontos para alimentar a CNN de classificação musical!