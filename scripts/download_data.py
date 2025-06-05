"""
Data Download Script

Downloads and prepares the music lyrics dataset from Kaggle.

Usage:
    python scripts/download_data.py
    python scripts/download_data.py --dataset "custom/dataset-name"
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data.data_loader import MusicDataLoader, load_music_dataset


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/data_download.log'),
            logging.StreamHandler()
        ]
    )


def main():
    """Main function to download and prepare data"""
    parser = argparse.ArgumentParser(description='Download music lyrics dataset')
    parser.add_argument(
        '--dataset',
        default='brianblakely/top-100-songs-and-lyrics-from-1959-to-2019',
        help='Kaggle dataset identifier'
    )
    parser.add_argument(
        '--file-path',
        default='',
        help='Specific file path within dataset'
    )
    parser.add_argument(
        '--data-dir',
        default='data',
        help='Data directory path'
    )
    parser.add_argument(
        '--force-download',
        action='store_true',
        help='Force re-download even if cached'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting data download process...")
        
        # Initialize data loader
        loader = MusicDataLoader(data_dir=args.data_dir)
        
        # Download dataset
        df = loader.load_kaggle_dataset(
            dataset_name=args.dataset,
            file_path=args.file_path,
            force_download=args.force_download
        )
        
        # Get dataset information
        info = loader.get_dataset_info(df)
        logger.info(f"Dataset info: {info}")
        
        # Validate dataset
        is_valid, issues = loader.validate_dataset(df)
        if not is_valid:
            logger.warning(f"Dataset validation issues found: {issues}")
        else:
            logger.info("Dataset validation passed!")
        
        # Display basic statistics
        print("\n" + "="*50)
        print("DATASET SUMMARY")
        print("="*50)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 records:")
        print(df.head())
        
        if 'year' in df.columns:
            print(f"\nYear range: {df['year'].min()} - {df['year'].max()}")
            print(f"Songs per decade:")
            decade_counts = (df['year'] // 10 * 10).value_counts().sort_index()
            for decade, count in decade_counts.items():
                print(f"  {decade}s: {count} songs")
        
        if 'artist' in df.columns:
            print(f"\nUnique artists: {df['artist'].nunique()}")
            print("Top 5 artists by song count:")
            top_artists = df['artist'].value_counts().head()
            for artist, count in top_artists.items():
                print(f"  {artist}: {count} songs")
        
        if 'lyrics' in df.columns:
            avg_length = df['lyrics'].str.len().mean()
            print(f"\nAverage lyrics length: {avg_length:.1f} characters")
        
        print("\n" + "="*50)
        print("Data download completed successfully!")
        print(f"Raw data saved in: {loader.raw_dir}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Error during data download: {str(e)}")
        raise


if __name__ == "__main__":
    main()