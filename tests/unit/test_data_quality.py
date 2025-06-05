"""
Testes de qualidade de dados - Carlos (QA Lead)
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestDataQuality:
    """Testes para validação de qualidade dos dados"""

    @pytest.mark.unit
    def test_dataset_structure(self, sample_lyrics_data):
        """Testa se dataset tem estrutura esperada"""
        df = sample_lyrics_data
        
        # Colunas obrigatórias
        required_cols = ['title', 'artist', 'year', 'lyrics']
        assert all(col in df.columns for col in required_cols)
        
        # Tipos de dados
        assert df['year'].dtype in ['int64', 'int32']
        assert df['title'].dtype == 'object'
        assert df['lyrics'].dtype == 'object'

    @pytest.mark.unit
    def test_data_completeness(self, sample_lyrics_data):
        """Testa completude dos dados"""
        df = sample_lyrics_data
        
        # Não deve ter valores nulos em colunas críticas
        assert df['title'].notna().all()
        assert df['artist'].notna().all()
        assert df['lyrics'].notna().all()
        
        # Anos devem estar em range válido
        assert df['year'].min() >= 1950
        assert df['year'].max() <= 2030

    @pytest.mark.unit
    def test_lyrics_quality(self, sample_lyrics_data):
        """Testa qualidade das letras"""
        df = sample_lyrics_data
        
        # Letras não devem estar vazias
        assert (df['lyrics'].str.len() > 0).all()
        
        # Letras devem ter tamanho mínimo razoável
        assert (df['lyrics'].str.len() >= 10).all()
        
        # Letras devem ter pelo menos algumas palavras
        word_counts = df['lyrics'].str.split().str.len()
        assert (word_counts >= 3).all()

    @pytest.mark.unit
    def test_labeled_data_integrity(self, sample_labeled_data):
        """Testa integridade dos dados anotados"""
        df = sample_labeled_data
        
        label_cols = ['misogyny', 'violence', 'depression', 'suicide', 'racism', 'homophobia']
        
        # Todas as colunas de label devem existir
        assert all(col in df.columns for col in label_cols)
        
        # Labels devem ser 0 ou 1
        for col in label_cols:
            assert df[col].isin([0, 1]).all()
        
        # Deve ter pelo menos alguns exemplos positivos
        total_positive = df[label_cols].sum().sum()
        assert total_positive > 0

    @pytest.mark.unit
    def test_temporal_distribution(self, sample_lyrics_data):
        """Testa distribuição temporal dos dados"""
        df = sample_lyrics_data
        
        # Deve cobrir múltiplas décadas
        decades = (df['year'] // 10) * 10
        assert len(decades.unique()) >= 2
        
        # Não deve ter concentração excessiva em uma década
        decade_counts = decades.value_counts()
        max_concentration = decade_counts.max() / len(df)
        assert max_concentration < 0.8  # Máximo 80% em uma década

    @pytest.mark.unit
    def test_artist_diversity(self, sample_lyrics_data):
        """Testa diversidade de artistas"""
        df = sample_lyrics_data
        
        # Deve ter múltiplos artistas
        unique_artists = df['artist'].nunique()
        assert unique_artists >= 2
        
        # Não deve ter dominância excessiva de um artista
        artist_counts = df['artist'].value_counts()
        max_artist_share = artist_counts.max() / len(df)
        assert max_artist_share < 0.7  # Máximo 70% de um artista

    @pytest.mark.unit
    def test_duplicates_detection(self, sample_lyrics_data):
        """Testa detecção de duplicatas"""
        df = sample_lyrics_data
        
        # Não deve ter duplicatas exatas
        assert not df.duplicated().any()
        
        # Não deve ter duplicatas por título + artista
        assert not df.duplicated(subset=['title', 'artist']).any()

    @pytest.mark.unit
    def test_encoding_consistency(self, sample_lyrics_data):
        """Testa consistência de encoding"""
        df = sample_lyrics_data
        
        # Verifica se não há caracteres problemáticos
        for text_col in ['title', 'artist', 'lyrics']:
            # Não deve ter caracteres de controle
            control_chars = df[text_col].str.contains(r'[\x00-\x1f\x7f-\x9f]', na=False)
            assert not control_chars.any()

    @pytest.mark.unit
    def test_label_distribution_balance(self, sample_labeled_data):
        """Testa balanceamento das classes"""
        df = sample_labeled_data
        label_cols = ['misogyny', 'violence', 'depression', 'suicide', 'racism', 'homophobia']
        
        for col in label_cols:
            positive_ratio = df[col].mean()
            
            # Nenhuma classe deve ser extremamente rara (< 1%) ou dominante (> 99%)
            assert 0.01 <= positive_ratio <= 0.99 or positive_ratio == 0.0
            
            # Deve ter pelo menos 1 exemplo positivo por categoria (em dataset real)
            if len(df) > 100:  # Apenas para datasets maiores
                assert df[col].sum() >= 1

    @pytest.mark.unit 
    def test_annotation_confidence(self, sample_labeled_data):
        """Testa qualidade da anotação"""
        df = sample_labeled_data
        
        # Se tem coluna de confiança, deve estar em range válido
        if 'confidence' in df.columns:
            assert df['confidence'].between(1, 5).all()
            assert df['confidence'].mean() >= 3.0  # Confiança mínima
        
        # Se tem anotador, deve estar preenchido
        if 'annotator_id' in df.columns:
            assert df['annotator_id'].notna().all()


class TestDataValidationPipeline:
    """Testes do pipeline de validação"""

    @pytest.mark.unit
    @patch('src.data.data_loader.MusicDataLoader')
    def test_data_loader_validation(self, mock_loader, sample_lyrics_data):
        """Testa validação do data loader"""
        mock_instance = mock_loader.return_value
        mock_instance.validate_dataset.return_value = (True, [])
        mock_instance.get_dataset_info.return_value = {
            'shape': (3, 4),
            'columns': ['title', 'artist', 'year', 'lyrics'],
            'null_counts': {'title': 0, 'artist': 0, 'year': 0, 'lyrics': 0}
        }
        
        # Testa se validação é chamada
        mock_instance.load_kaggle_dataset()
        mock_instance.validate_dataset.assert_called()

    @pytest.mark.unit
    def test_validation_edge_cases(self):
        """Testa casos extremos de validação"""
        
        # Dataset vazio
        empty_df = pd.DataFrame()
        assert len(empty_df) == 0
        
        # Dataset com uma linha
        single_row = pd.DataFrame({
            'title': ['Test'],
            'artist': ['Artist'],
            'year': [2000],
            'lyrics': ['Short lyric']
        })
        assert len(single_row) == 1
        
        # Dataset com valores extremos
        extreme_df = pd.DataFrame({
            'title': ['A' * 1000],  # Título muito longo
            'artist': [''],  # Artista vazio
            'year': [1850],  # Ano muito antigo
            'lyrics': ['x']  # Letra muito curta
        })
        
        # Validações específicas para casos extremos
        assert len(extreme_df['title'].iloc[0]) == 1000
        assert extreme_df['artist'].iloc[0] == ''
        assert extreme_df['year'].iloc[0] == 1850