# Models Directory

## Overview
This directory stores trained models, checkpoints, and experiment artifacts.

## Structure

### `/trained`
- Final trained models ready for deployment
- Model artifacts with metadata
- Performance benchmarks

### `/experiments` 
- Experimental model variants
- Hyperparameter tuning results
- A/B testing artifacts

### `/checkpoints`
- Training checkpoints for resuming
- Best model states during training
- Early stopping artifacts

## Model Naming Convention

```
{architecture}_{dataset}_{timestamp}_{performance}.{ext}
```

Examples:
- `lstm_music_20231201_f1_0.85.pt`
- `cnn_lyrics_20231201_acc_0.82.pkl`
- `transformer_distilbert_20231201_auc_0.88.bin`

## Version Control

- Use DVC or Git LFS for large model files
- Track model lineage and experiment metadata
- Maintain model performance logs