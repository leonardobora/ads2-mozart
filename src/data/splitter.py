"""
Data Splitting Module

Provides stratified splitting of music data considering temporal, genre, 
and label distribution aspects for robust train/validation/test sets.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from typing import Tuple, Optional
import warnings


def create_stratified_split(
    df: pd.DataFrame,
    test_size: float = 0.2,
    val_size: float = 0.1,
    stratify_by: str = 'decade',
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Cria divisão estratificada dos dados musicais
    
    Args:
        df: DataFrame com dados musicais
        test_size: Proporção para teste (0.2 = 20%)
        val_size: Proporção para validação (0.1 = 10%)
        stratify_by: Coluna para estratificação ('decade', 'year', 'genre')
        random_state: Seed para reprodutibilidade
        
    Returns:
        Tuple com (train_df, val_df, test_df)
    """
    
    # Cria coluna de década se necessário
    if stratify_by == 'decade' and 'decade' not in df.columns and 'year' in df.columns:
        df = df.copy()
        df['decade'] = (df['year'] // 10) * 10
    
    # Verifica se coluna de estratificação existe
    if stratify_by not in df.columns:
        warnings.warn(f"Coluna '{stratify_by}' não encontrada. Usando divisão aleatória.")
        stratify_col = None
    else:
        stratify_col = df[stratify_by]
    
    # Primeira divisão: treino+val vs teste
    train_val_df, test_df = train_test_split(
        df,
        test_size=test_size,
        stratify=stratify_col,
        random_state=random_state
    )
    
    # Segunda divisão: treino vs validação
    # Ajusta proporção da validação
    val_size_adjusted = val_size / (1 - test_size)
    
    if stratify_by in train_val_df.columns:
        stratify_col_train_val = train_val_df[stratify_by]
    else:
        stratify_col_train_val = None
    
    train_df, val_df = train_test_split(
        train_val_df,
        test_size=val_size_adjusted,
        stratify=stratify_col_train_val,
        random_state=random_state
    )
    
    print(f"✅ Divisão dos dados criada:")
    print(f"   📚 Treino: {len(train_df)} músicas ({len(train_df)/len(df)*100:.1f}%)")
    print(f"   🔍 Validação: {len(val_df)} músicas ({len(val_df)/len(df)*100:.1f}%)")
    print(f"   🧪 Teste: {len(test_df)} músicas ({len(test_df)/len(df)*100:.1f}%)")
    
    if stratify_by in df.columns:
        print(f"\n📊 Distribuição por {stratify_by}:")
        for name, data in [("Treino", train_df), ("Validação", val_df), ("Teste", test_df)]:
            dist = data[stratify_by].value_counts().sort_index()
            print(f"   {name}: {dict(dist)}")
    
    return train_df, val_df, test_df


def balance_dataset(df: pd.DataFrame, target_cols: list, method: str = 'undersample') -> pd.DataFrame:
    """
    Balanceia dataset para classificação de múltiplos rótulos
    
    Args:
        df: DataFrame com dados
        target_cols: Lista de colunas de rótulos
        method: 'undersample' ou 'oversample'
        
    Returns:
        DataFrame balanceado
    """
    
    if method == 'undersample':
        # Encontra classe minoritária
        min_count = float('inf')
        for col in target_cols:
            if col in df.columns:
                positive_count = df[col].sum()
                min_count = min(min_count, positive_count)
        
        # Subamostra cada classe
        balanced_dfs = []
        for col in target_cols:
            if col in df.columns:
                positive_samples = df[df[col] == 1].sample(min_count)
                negative_samples = df[df[col] == 0].sample(min_count)
                balanced_dfs.extend([positive_samples, negative_samples])
        
        # Combina e remove duplicatas
        balanced_df = pd.concat(balanced_dfs).drop_duplicates()
        
    else:  # oversample
        # Implementação simples de oversampling
        # Para implementação mais sofisticada, usar SMOTE
        balanced_df = df.copy()
        
        for col in target_cols:
            if col in df.columns:
                positive_samples = df[df[col] == 1]
                negative_samples = df[df[col] == 0]
                
                # Duplica classe minoritária
                if len(positive_samples) < len(negative_samples):
                    multiplier = len(negative_samples) // len(positive_samples)
                    balanced_df = pd.concat([balanced_df] + [positive_samples] * multiplier)
                elif len(negative_samples) < len(positive_samples):
                    multiplier = len(positive_samples) // len(negative_samples)
                    balanced_df = pd.concat([balanced_df] + [negative_samples] * multiplier)
    
    return balanced_df.reset_index(drop=True)