"""
Configuração global para testes pytest
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil


@pytest.fixture(scope="session")
def test_data_dir():
    """Diretório para dados de teste"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def sample_lyrics_data():
    """Dataset de exemplo para testes"""
    data = {
        'title': ['Test Song 1', 'Test Song 2', 'Test Song 3'],
        'artist': ['Artist A', 'Artist B', 'Artist C'],
        'year': [1990, 2000, 2010],
        'lyrics': [
            'This is a clean song about love and happiness',
            'This song contains some violence and anger',
            'A sad song about depression and loneliness'
        ]
    }
    return pd.DataFrame(data)


@pytest.fixture(scope="session")
def sample_labeled_data():
    """Dataset anotado para testes"""
    data = {
        'title': ['Test Song 1', 'Test Song 2', 'Test Song 3'],
        'artist': ['Artist A', 'Artist B', 'Artist C'],
        'year': [1990, 2000, 2010],
        'lyrics': [
            'This is a clean song about love',
            'This song contains violence',
            'A sad song about depression'
        ],
        'misogyny': [0, 0, 0],
        'violence': [0, 1, 0],
        'depression': [0, 0, 1],
        'suicide': [0, 0, 0],
        'racism': [0, 0, 0],
        'homophobia': [0, 0, 0]
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_dir():
    """Diretório temporário para testes"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_config():
    """Configuração mock para testes"""
    return {
        'data': {
            'raw_data_path': 'tests/fixtures/',
            'processed_data_path': 'tests/fixtures/',
            'test_size': 0.2,
            'val_size': 0.1,
            'random_state': 42
        },
        'text_processing': {
            'max_sequence_length': 100,
            'vocab_size': 1000,
            'min_word_freq': 1,
            'lowercase': True
        },
        'model': {
            'type': 'cnn',
            'filter_sizes': [2, 3, 4],
            'num_filters': 32,
            'dropout': 0.5,
            'embedding_dim': 50,
            'num_classes': 6
        },
        'training': {
            'batch_size': 4,
            'learning_rate': 0.001,
            'epochs': 2,
            'patience': 1
        }
    }


@pytest.fixture
def mock_model_weights():
    """Pesos mock para teste de modelo"""
    return {
        'embedding.weight': np.random.randn(1000, 50),
        'conv_layers.0.weight': np.random.randn(32, 1, 2, 50),
        'fc.weight': np.random.randn(6, 96),
        'fc.bias': np.random.randn(6)
    }


# Markers personalizados
def pytest_configure(config):
    """Configurações personalizadas do pytest"""
    config.addinivalue_line(
        "markers", "slow: marca testes que demoram para executar"
    )
    config.addinivalue_line(
        "markers", "integration: marca testes de integração"
    )
    config.addinivalue_line(
        "markers", "unit: marca testes unitários"
    )
    config.addinivalue_line(
        "markers", "performance: marca testes de performance"
    )
    config.addinivalue_line(
        "markers", "security: marca testes de segurança"
    )


# Configuração de logging para testes
import logging
logging.getLogger().setLevel(logging.WARNING)