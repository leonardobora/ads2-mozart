# Data Directory Structure

## Overview
This directory contains all data related to the music content classification project.

## Directory Structure

### `/raw`
- Original, immutable data dump
- Music lyrics datasets (1959-2023)
- Metadata files (artist, year, genre, etc.)
- **Never edit files in this directory**

### `/external`
- Data from third-party sources
- Pre-trained embeddings
- External music databases

### `/interim`
- Intermediate data that has been transformed
- Cleaned text files
- Tokenized lyrics

### `/processed`
- Final datasets ready for modeling
- Train/validation/test splits
- Feature matrices
- Encoded target labels

### `/labeled`
- Human-annotated datasets
- Ground truth labels for sensitive content
- Inter-annotator agreement scores

## Data Security
- All sensitive content is gitignored
- Use data anonymization when possible
- Follow ethical guidelines for music content analysis