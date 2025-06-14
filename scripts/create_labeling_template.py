# -*- coding: utf-8 -*-
"""
Script para Criar Template de Rotulação

Cria arquivo estruturado para rotulação manual de conteúdo sensível em letras musicais.

Uso:
    python scripts/create_labeling_template.py --sample 1000 --output data/labeled/
"""

import argparse
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from data.data_loader import MusicDataLoader


def create_labeling_template(input_path: str, sample_size: int, output_dir: str):
    """
    Cria template de rotulação com amostra estratificada
    
    Args:
        input_path: Caminho para dados processados
        sample_size: Número de músicas para rotular
        output_dir: Diretório de saída
    """
    
    # Carrega dados processados
    loader = MusicDataLoader()
    
    # Tenta encontrar arquivo de dados
    possible_files = [
        f"{input_path}/music_lyrics_cleaned.csv",
        f"{input_path}/train_data.csv", 
        "data/raw/kaggle_brianblakely_top-100-songs-and-lyrics-from-1959-to-2019.csv"
    ]
    
    df = None
    for file_path in possible_files:
        try:
            df = pd.read_csv(file_path)
            print(f"✅ Dados carregados de: {file_path}")
            break
        except FileNotFoundError:
            continue
    
    if df is None:
        raise FileNotFoundError("Nenhum arquivo de dados encontrado!")
    
    # Amostragem estratificada por década
    if 'year' in df.columns:
        df['decade'] = (df['year'] // 10) * 10
        # Amostra proporcional por década
        sampled_df = df.groupby('decade').apply(
            lambda x: x.sample(min(len(x), sample_size // df['decade'].nunique()))
        ).reset_index(drop=True)
    else:
        # Amostragem aleatória simples
        sampled_df = df.sample(min(sample_size, len(df)))
    
    # Mapeia nomes de colunas para nomes padronizados
    column_mapping = {
        'Song Title': 'title',
        'Artist': 'artist', 
        'Year': 'year',
        'Lyrics': 'lyrics'
    }
    
    # Renomeia as colunas
    sampled_df = sampled_df.rename(columns=column_mapping)
    
    # Cria template de rotulação
    labeling_df = sampled_df[['title', 'artist', 'year', 'lyrics']].copy()
    
    # Adiciona coluna de rótulo para misoginia (0-1 continuous scale)
    labeling_df['misogyny_score'] = None  # Para preenchimento manual (0.0 - 1.0)
    
    # Adiciona colunas auxiliares
    labeling_df['annotator_id'] = None
    labeling_df['confidence'] = None  # 1-5 scale
    labeling_df['notes'] = None
    labeling_df['lyrics_preview'] = labeling_df['lyrics'].str[:200] + "..."
    
    # Reorganiza colunas
    cols = ['title', 'artist', 'year', 'lyrics_preview', 'misogyny_score', 'annotator_id', 'confidence', 'notes', 'lyrics']
    labeling_df = labeling_df[cols]
    
    # Salva template
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    template_file = output_path / "songs_to_label.csv"
    labeling_df.to_csv(template_file, index=False)
    
    # Cria arquivo de instruções
    instructions_file = output_path / "INSTRUCTIONS_PT.md"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write("""# 📝 Instruções para Rotulação de Misoginia em Letras Musicais

## Objetivo
Identificar e classificar conteúdo misógino nas letras musicais para treinar modelo CNN.
**FOCO EXCLUSIVO**: Misoginia (conteúdo que degrada, objetifica ou promove violência contra mulheres)

## Escala de Classificação

### **misogyny_score**: Valor contínuo entre 0.0 e 1.0

#### **0.0 - Baixo/Ausente**
- Nenhum conteúdo misógino detectável
- Menções neutras ou positivas de mulheres
- Exemplo: "She's amazing", "My mother taught me"

#### **0.3 - Médio** 
- Insinuações sutis de inferioridade feminina
- Estereótipos de gênero problemáticos
- Exemplo: "Women belong in the kitchen", "Girls are too emotional"

#### **0.7 - Médio Alto**
- Objetificação sexual explícita
- Linguagem degradante sobre mulheres
- Exemplo: "She's just a toy", "Women are for pleasure"

#### **1.0 - Alto**
- Promoção direta de violência contra mulheres
- Conteúdo extremamente degradante
- Linguagem violenta e misógina explícita
- Exemplo: Threats of violence, extreme sexual degradation

## Como Rotular

### 1. Leia a letra completa cuidadosamente
### 2. Atribua um score de 0.0 a 1.0 na coluna **misogyny_score**
### 3. Preencha campos obrigatórios:
- **annotator_id**: Suas iniciais
- **confidence**: 1-5 (1=muito incerto, 5=muito certo)
- **notes**: Justificativa da pontuação (opcional mas recomendado)

## Critérios Importantes:
- ✅ Considere o contexto completo da música
- ✅ Foque apenas em conteúdo contra mulheres/feminino
- ✅ Seja consistente na escala
- ✅ Use valores intermediários (0.1, 0.2, 0.4, 0.6, 0.8, 0.9)
- ❌ NÃO considere palavrões gerais que não sejam misóginos
- ❌ NÃO rotule baseado no gênero musical ou época

## Exemplos de Pontuação:

**Score 0.0**: "She's the love of my life, so beautiful and smart"
**Score 0.3**: "Women always complain about everything"  
**Score 0.7**: "She's nothing but a piece of meat to me"
**Score 1.0**: [Conteúdo extremamente violento - censurado]

## ⚠️ Importante
- Este trabalho é para fins acadêmicos de classificação de conteúdo
- Consulte supervisor se encontrar conteúdo extremamente perturbador
- Mantenha objetividade e consistência nas avaliações
""")

    print(f"✅ Template criado: {template_file}")
    print(f"✅ Instruções: {instructions_file}")
    print(f"📊 Total de músicas para rotular: {len(labeling_df)}")
    
    if 'decade' in labeling_df.columns:
        print("\n📈 Distribuição por década:")
        decade_dist = labeling_df['decade'].value_counts().sort_index()
        for decade, count in decade_dist.items():
            print(f"  {decade}s: {count} músicas")


def main():
    parser = argparse.ArgumentParser(description='Criar template de rotulação')
    parser.add_argument('--sample', type=int, default=1000, help='Número de músicas para rotular')
    parser.add_argument('--input', default='data/processed', help='Diretório de dados processados')
    parser.add_argument('--output', default='data/labeled', help='Diretório de saída')
    
    args = parser.parse_args()
    
    create_labeling_template(
        input_path=args.input,
        sample_size=args.sample,
        output_dir=args.output
    )


if __name__ == "__main__":
    main()