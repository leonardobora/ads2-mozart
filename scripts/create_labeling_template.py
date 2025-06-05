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
    
    # Cria template de rotulação
    labeling_df = sampled_df[['title', 'artist', 'year', 'lyrics']].copy()
    
    # Adiciona colunas de rótulos (0/1 para cada categoria)
    labels = ['misogyny', 'violence', 'depression', 'suicide', 'racism', 'homophobia']
    for label in labels:
        labeling_df[label] = None  # Para preenchimento manual
    
    # Adiciona colunas auxiliares
    labeling_df['annotator_id'] = None
    labeling_df['confidence'] = None  # 1-5 scale
    labeling_df['notes'] = None
    labeling_df['lyrics_preview'] = labeling_df['lyrics'].str[:200] + "..."
    
    # Reorganiza colunas
    cols = ['title', 'artist', 'year', 'lyrics_preview'] + labels + ['annotator_id', 'confidence', 'notes', 'lyrics']
    labeling_df = labeling_df[cols]
    
    # Salva template
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    template_file = output_path / "songs_to_label.csv"
    labeling_df.to_csv(template_file, index=False)
    
    # Cria arquivo de instruções
    instructions_file = output_path / "INSTRUCTIONS_PT.md"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write("""# 📝 Instruções para Rotulação de Conteúdo Sensível

## Objetivo
Identificar conteúdo sensível nas letras musicais para treinar modelo CNN.

## Como Rotular

### 1. Para cada música, marque 1 (presente) ou 0 (ausente) para:

**misogyny**: Conteúdo que degrada, objetifica ou promove violência contra mulheres
- Exemplos: "women are objects", "she's just a toy", linguagem sexualmente degradante

**violence**: Descrições de violência física, armas, agressões
- Exemplos: referencias a armas, brigas, assassinatos, violência urbana

**depression**: Conteúdo relacionado à depressão, tristeza profunda, desesperança
- Exemplos: "I want to disappear", "nothing matters anymore", sentimentos de vazio

**suicide**: Referencias diretas ou indiretas ao suicídio
- Exemplos: "end it all", "better off dead", métodos de autolesão

**racism**: Conteúdo racista, preconceituoso ou discriminatório
- Exemplos: slurs raciais, estereótipos negativos, supremacismo

**homophobia**: Conteúdo homofóbico ou discriminatório contra LGBTQ+
- Exemplos: slurs homofóbicos, discriminação por orientação sexual

### 2. Preencha campos adicionais:
- **annotator_id**: Seu nome/iniciais
- **confidence**: 1-5 (1=incerto, 5=muito certo)
- **notes**: Observações especiais

### 3. Critérios Importantes:
- ❌ NÃO rotule baseado no gênero musical
- ❌ NÃO rotule palavrões simples (a menos que sejam ofensivos)
- ✅ Considere o contexto completo da música
- ✅ Seja consistente nos critérios
- ✅ Quando em dúvida, marque confidence baixa

## Exemplos

### Música COM conteúdo sensível:
**Título**: "Exemplo Song"
- violence: 1 (menciona "gun" e "kill")
- misogyny: 1 (chama mulheres de "objects")
- depression: 0
- suicide: 0
- racism: 0
- homophobia: 0

### Música SEM conteúdo sensível:
**Título**: "Love Song"
- Todos os campos: 0 (música romântica sem conteúdo problemático)

## ⚠️ Importante
Este trabalho é para fins acadêmicos de pesquisa sobre conteúdo musical.
Consulte supervisor se encontrar conteúdo extremamente perturbador.
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