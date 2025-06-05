"""
Data Loading and Management Module

This module handles loading and basic processing of music lyrics datasets.
Supports multiple data formats and provides standardized data access.
"""

import os
import pandas as pd
import numpy as np
from typing import Optional, Tuple, Dict, Any
import logging
from pathlib import Path

try:
    import kagglehub
    from kagglehub import KaggleDatasetAdapter
    KAGGLE_AVAILABLE = True
except ImportError:
    KAGGLE_AVAILABLE = False
    logging.warning("kagglehub not available. Install with: pip install kagglehub[pandas-datasets]")


class MusicDataLoader:
    """
    Main data loader for music lyrics datasets
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.logger = logging.getLogger(__name__)
        
        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def load_kaggle_dataset(
        self, 
        dataset_name: str = "brianblakely/top-100-songs-and-lyrics-from-1959-to-2019",
        file_path: str = "",
        force_download: bool = False
    ) -> pd.DataFrame:
        """
        Load dataset from Kaggle using kagglehub
        
        Args:
            dataset_name: Kaggle dataset identifier
            file_path: Specific file path within dataset (if any)
            force_download: Force re-download even if cached
            
        Returns:
            pandas.DataFrame: Loaded dataset
        """
        if not KAGGLE_AVAILABLE:
            raise ImportError("kagglehub not available. Install with: pip install kagglehub[pandas-datasets]")
        
        try:
            self.logger.info(f"Loading Kaggle dataset: {dataset_name}")
            
            # Load the dataset using kagglehub
            df = kagglehub.load_dataset(
                KaggleDatasetAdapter.PANDAS,
                dataset_name,
                file_path
            )
            
            self.logger.info(f"Dataset loaded successfully. Shape: {df.shape}")
            self.logger.info(f"Columns: {list(df.columns)}")
            
            # Save raw data locally
            raw_file_path = self.raw_dir / f"kaggle_{dataset_name.replace('/', '_')}.csv"
            df.to_csv(raw_file_path, index=False)
            self.logger.info(f"Raw data saved to: {raw_file_path}")
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading Kaggle dataset: {str(e)}")
            raise
    
    def load_local_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load dataset from local CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            pandas.DataFrame: Loaded dataset
        """
        try:
            df = pd.read_csv(file_path)
            self.logger.info(f"Local CSV loaded. Shape: {df.shape}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading local CSV: {str(e)}")
            raise
    
    def get_dataset_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get basic information about the dataset
        
        Args:
            df: Input dataframe
            
        Returns:
            Dict containing dataset statistics
        """
        info = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "text_columns": df.select_dtypes(include=['object']).columns.tolist()
        }
        
        # Additional music-specific info
        if 'year' in df.columns:
            info['year_range'] = (df['year'].min(), df['year'].max())
            info['year_distribution'] = df['year'].value_counts().head(10).to_dict()
        
        if 'artist' in df.columns:
            info['unique_artists'] = df['artist'].nunique()
            info['top_artists'] = df['artist'].value_counts().head(10).to_dict()
        
        if 'lyrics' in df.columns:
            info['avg_lyrics_length'] = df['lyrics'].str.len().mean()
            info['lyrics_length_std'] = df['lyrics'].str.len().std()
        
        return info
    
    def validate_dataset(self, df: pd.DataFrame) -> Tuple[bool, list]:
        """
        Validate dataset structure and content
        
        Args:
            df: Input dataframe
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check required columns
        required_columns = ['title', 'artist', 'year', 'lyrics']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            issues.append(f"Missing required columns: {missing_cols}")
        
        # Check for empty lyrics
        if 'lyrics' in df.columns:
            empty_lyrics = df['lyrics'].isnull().sum()
            if empty_lyrics > 0:
                issues.append(f"Found {empty_lyrics} songs with empty lyrics")
        
        # Check year range
        if 'year' in df.columns:
            min_year, max_year = df['year'].min(), df['year'].max()
            if min_year < 1900 or max_year > 2030:
                issues.append(f"Suspicious year range: {min_year}-{max_year}")
        
        # Check duplicates
        if 'title' in df.columns and 'artist' in df.columns:
            duplicates = df.duplicated(subset=['title', 'artist']).sum()
            if duplicates > 0:
                issues.append(f"Found {duplicates} duplicate songs (same title + artist)")
        
        is_valid = len(issues) == 0
        return is_valid, issues


def load_music_dataset(config_path: Optional[str] = None) -> pd.DataFrame:
    """
    Convenience function to load music dataset based on configuration
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        pandas.DataFrame: Loaded dataset
    """
    loader = MusicDataLoader()
    
    # Default to Kaggle dataset
    df = loader.load_kaggle_dataset()
    
    # Validate the dataset
    is_valid, issues = loader.validate_dataset(df)
    if not is_valid:
        logging.warning(f"Dataset validation issues: {issues}")
    
    return df