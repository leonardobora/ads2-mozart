# Data Format Specification

## Input Data Format

### Raw Lyrics Data
Expected CSV format with columns:
- `song_id`: Unique identifier
- `title`: Song title
- `artist`: Artist name
- `year`: Release year
- `genre`: Music genre
- `lyrics`: Full song lyrics text
- `album`: Album name (optional)

### Labeled Data Format
CSV format with additional columns:
- `misogyny`: Binary label (0/1)
- `violence`: Binary label (0/1) 
- `depression`: Binary label (0/1)
- `suicide`: Binary label (0/1)
- `racism`: Binary label (0/1)
- `homophobia`: Binary label (0/1)
- `annotator_id`: Human annotator identifier
- `confidence`: Annotation confidence score

## Processed Data Format

### Feature Matrices
- Sparse matrices for TF-IDF features
- Dense arrays for embeddings
- Temporal features as structured arrays

### Model Inputs
- Tokenized sequences (integer arrays)
- Attention masks for transformers
- Metadata features as additional inputs

## File Naming Conventions

- Raw data: `music_lyrics_YYYY.csv`
- Processed: `processed_features_YYYY_MM_DD.npz`
- Splits: `train_data.csv`, `val_data.csv`, `test_data.csv`