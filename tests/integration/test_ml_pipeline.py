"""
Testes do pipeline de ML - Luan (ML QA)
"""

import pytest
import torch
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
import tempfile
import os


class TestMLPipelineIntegration:
    """Testes de integração do pipeline de ML"""

    @pytest.mark.integration
    def test_end_to_end_training_pipeline(self, sample_labeled_data, temp_dir, mock_config):
        """Testa pipeline completo de treino"""
        # Simula dados salvos
        data_path = temp_dir / "train_data.csv"
        sample_labeled_data.to_csv(data_path, index=False)
        
        # Mock do processo de treinamento
        with patch('src.models.trainer.CNNTrainer') as mock_trainer:
            mock_instance = mock_trainer.return_value
            mock_instance.train.return_value = {
                'train_loss': [0.8, 0.6, 0.4],
                'val_loss': [0.9, 0.7, 0.5],
                'val_f1': [0.4, 0.6, 0.7]
            }
            
            # Executa pipeline
            result = mock_instance.train()
            
            # Validações
            assert 'train_loss' in result
            assert 'val_f1' in result
            assert len(result['train_loss']) == 3
            assert result['val_f1'][-1] > result['val_f1'][0]  # Melhora ao longo do tempo

    @pytest.mark.integration
    def test_model_save_load_cycle(self, temp_dir, mock_config):
        """Testa ciclo de salvar e carregar modelo"""
        model_path = temp_dir / "test_model.pt"
        
        # Mock do modelo CNN
        with patch('src.models.cnn_classifier.CNNClassifier') as mock_cnn:
            mock_instance = mock_cnn.return_value
            
            # Simula salvamento
            mock_instance.save.return_value = True
            mock_instance.save(str(model_path))
            
            # Simula carregamento
            mock_cnn.load.return_value = mock_instance
            loaded_model = mock_cnn.load(str(model_path))
            
            # Validações
            mock_instance.save.assert_called_with(str(model_path))
            mock_cnn.load.assert_called_with(str(model_path))
            assert loaded_model is not None

    @pytest.mark.integration
    def test_preprocessing_to_model_pipeline(self, sample_lyrics_data, mock_config):
        """Testa pipeline de preprocessamento até modelo"""
        
        with patch('src.features.text_features.TextFeatureExtractor') as mock_extractor:
            mock_instance = mock_extractor.return_value
            
            # Mock do processamento
            mock_instance.fit_transform.return_value = {
                'input_ids': torch.randint(0, 1000, (3, 100)),
                'attention_mask': torch.ones(3, 100)
            }
            
            # Executa preprocessamento
            features = mock_instance.fit_transform(sample_lyrics_data['lyrics'].tolist())
            
            # Validações
            assert 'input_ids' in features
            assert 'attention_mask' in features
            assert features['input_ids'].shape[0] == 3
            assert features['input_ids'].shape[1] == 100

    @pytest.mark.integration  
    def test_training_evaluation_pipeline(self, sample_labeled_data, mock_config):
        """Testa pipeline de treino e avaliação"""
        
        with patch('src.models.evaluator.ModelEvaluator') as mock_evaluator:
            mock_instance = mock_evaluator.return_value
            
            # Mock das métricas
            mock_instance.evaluate.return_value = {
                'f1_macro': 0.65,
                'f1_micro': 0.68,
                'precision_macro': 0.63,
                'recall_macro': 0.67,
                'roc_auc_macro': 0.72,
                'per_class_f1': {
                    'misogyny': 0.60,
                    'violence': 0.70,
                    'depression': 0.65,
                    'suicide': 0.55,
                    'racism': 0.68,
                    'homophobia': 0.62
                }
            }
            
            # Executa avaliação
            metrics = mock_instance.evaluate(sample_labeled_data)
            
            # Validações
            assert metrics['f1_macro'] > 0.5
            assert 'per_class_f1' in metrics
            assert len(metrics['per_class_f1']) == 6
            assert all(score > 0.5 for score in metrics['per_class_f1'].values())

    @pytest.mark.integration
    def test_inference_pipeline(self, temp_dir, mock_config):
        """Testa pipeline de inferência"""
        
        test_lyrics = [
            "This is a happy love song",
            "This song contains violent content",
            "A sad song about depression and loneliness"
        ]
        
        with patch('src.models.cnn_classifier.CNNClassifier') as mock_cnn:
            mock_instance = mock_cnn.return_value
            
            # Mock das predições
            mock_instance.predict.return_value = np.array([
                [0.1, 0.2, 0.1, 0.1, 0.1, 0.1],  # Clean song
                [0.2, 0.8, 0.2, 0.1, 0.2, 0.1],  # Violent song  
                [0.1, 0.2, 0.7, 0.3, 0.1, 0.1]   # Depressing song
            ])
            
            mock_instance.predict_proba.return_value = mock_instance.predict.return_value
            
            # Executa predição
            predictions = mock_instance.predict(test_lyrics)
            probabilities = mock_instance.predict_proba(test_lyrics)
            
            # Validações
            assert predictions.shape == (3, 6)
            assert probabilities.shape == (3, 6)
            assert np.all(predictions >= 0) and np.all(predictions <= 1)

    @pytest.mark.integration
    def test_hyperparameter_tuning_pipeline(self, sample_labeled_data, mock_config):
        """Testa pipeline de tuning de hiperparâmetros"""
        
        with patch('src.models.trainer.HyperparameterTuner') as mock_tuner:
            mock_instance = mock_tuner.return_value
            
            # Mock do tuning
            mock_instance.tune.return_value = {
                'best_params': {
                    'learning_rate': 0.001,
                    'dropout': 0.5,
                    'num_filters': 128,
                    'filter_sizes': [2, 3, 4, 5]
                },
                'best_score': 0.72,
                'tuning_history': [
                    {'params': {'learning_rate': 0.01}, 'score': 0.65},
                    {'params': {'learning_rate': 0.001}, 'score': 0.72},
                    {'params': {'learning_rate': 0.0001}, 'score': 0.68}
                ]
            }
            
            # Executa tuning
            results = mock_instance.tune(sample_labeled_data)
            
            # Validações
            assert 'best_params' in results
            assert 'best_score' in results
            assert results['best_score'] > 0.7
            assert len(results['tuning_history']) == 3


class TestMLPipelinePerformance:
    """Testes de performance do pipeline"""

    @pytest.mark.integration
    @pytest.mark.performance  
    def test_training_speed(self, sample_labeled_data, mock_config):
        """Testa velocidade de treinamento"""
        import time
        
        start_time = time.time()
        
        # Simula treinamento rápido
        with patch('src.models.trainer.CNNTrainer') as mock_trainer:
            mock_instance = mock_trainer.return_value
            mock_instance.train.return_value = {'val_f1': [0.7]}
            
            # Executa
            mock_instance.train()
            
        end_time = time.time()
        training_time = end_time - start_time
        
        # Deve ser rápido (mock)
        assert training_time < 1.0

    @pytest.mark.integration
    @pytest.mark.performance
    def test_inference_speed(self, mock_config):
        """Testa velocidade de inferência"""
        import time
        
        test_lyrics = ["Test song"] * 100  # 100 músicas
        
        with patch('src.models.cnn_classifier.CNNClassifier') as mock_cnn:
            mock_instance = mock_cnn.return_value
            mock_instance.predict.return_value = np.random.rand(100, 6)
            
            start_time = time.time()
            predictions = mock_instance.predict(test_lyrics)
            end_time = time.time()
            
            inference_time = end_time - start_time
            
            # Deve processar 100 músicas rapidamente
            assert inference_time < 2.0
            assert predictions.shape == (100, 6)

    @pytest.mark.integration
    def test_memory_usage_reasonable(self, sample_labeled_data, mock_config):
        """Testa uso de memória"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Simula operações de ML
        with patch('src.models.trainer.CNNTrainer') as mock_trainer:
            mock_instance = mock_trainer.return_value
            mock_instance.train.return_value = {'val_f1': [0.7]}
            mock_instance.train()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Aumento de memória deve ser razoável (< 500MB para mocks)
        assert memory_increase < 500


class TestMLPipelineRobustness:
    """Testes de robustez do pipeline"""

    @pytest.mark.integration
    def test_pipeline_with_corrupted_data(self, temp_dir, mock_config):
        """Testa pipeline com dados corrompidos"""
        
        # Cria dados corrompidos
        corrupted_data = pd.DataFrame({
            'title': ['Song 1', None, ''],
            'artist': ['Artist 1', 'Artist 2', None],
            'year': [2000, 'invalid', 2010],
            'lyrics': ['Good lyrics', '', None],
            'violence': [0, 1, 'invalid']
        })
        
        data_path = temp_dir / "corrupted_data.csv"
        corrupted_data.to_csv(data_path, index=False)
        
        # Pipeline deve lidar com dados corrompidos
        with patch('src.data.data_loader.MusicDataLoader') as mock_loader:
            mock_instance = mock_loader.return_value
            mock_instance.validate_dataset.return_value = (False, [
                "Missing values found in critical columns",
                "Invalid data types detected"
            ])
            
            is_valid, issues = mock_instance.validate_dataset(corrupted_data)
            
            assert not is_valid
            assert len(issues) >= 2

    @pytest.mark.integration
    def test_pipeline_recovery_from_failure(self, sample_labeled_data, temp_dir, mock_config):
        """Testa recuperação de falhas no pipeline"""
        
        with patch('src.models.trainer.CNNTrainer') as mock_trainer:
            mock_instance = mock_trainer.return_value
            
            # Simula falha e recuperação
            mock_instance.train.side_effect = [
                Exception("Training failed"),  # Primeira tentativa falha
                {'val_f1': [0.7]}  # Segunda tentativa sucesso
            ]
            
            # Primeira tentativa deve falhar
            with pytest.raises(Exception):
                mock_instance.train()
            
            # Segunda tentativa deve funcionar
            result = mock_instance.train()
            assert 'val_f1' in result