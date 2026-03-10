import os
import shutil
from src.logger.logger import logging
import pandas as pd
from pathlib import Path
from datetime import datetime

# Define base paths
BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

class DataIngestion:
    def __init__(self, landing_dir: str, archive_dir: str, processed_dir: str):
        self.landing_dir = Path(landing_dir)
        self.archive_dir = Path(archive_dir)
        self.processed_dir = Path(processed_dir)
        
        # Ensure directories exist
        self.landing_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def process_landing_zone(self):
        """Scans the landing zone for .xlsx files, converts them to parquet, and archives them."""
        new_files = list(self.landing_dir.glob('*.xlsx'))
        
        if not new_files:
            logging.info("No new files found in the landing zone.")
            return

        for file_path in new_files:
            logging.info(f"Processing new file: {file_path.name}")
            self._convert_and_save(file_path)
            self._archive_file(file_path)

    def _convert_and_save(self, file_path: Path):
        """Reads Excel and saves as Parquet."""
        try:
            # Read the Excel file
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # Generate a clean filename based on timestamp to avoid overwrites
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_stem = file_path.stem
            parquet_filename = f"{file_stem}_{timestamp}.parquet"
            parquet_path = self.processed_dir / parquet_filename
            
            # Save to Parquet
            df.to_parquet(parquet_path, index=False, engine='pyarrow')
            logging.info(f"Successfully saved to {parquet_path}")
            
        except Exception as e:
            logging.error(f"Failed to process {file_path.name}. Error: {e}")
            raise

    def _archive_file(self, file_path: Path):
        """Moves the processed file to the archive directory."""
        archive_path = self.archive_dir / file_path.name
        # Handle case where file already exists in archive
        if archive_path.exists():
            archive_path = self.archive_dir / f"{file_path.stem}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
            
        shutil.move(str(file_path), str(archive_path))
        logging.info(f"Archived {file_path.name} to {self.archive_dir}")

if __name__ == "__main__":
    # Define paths relative to the project root
    BASE_DIR = Path(__file__).resolve().parents[2]
    LANDING = BASE_DIR / "data" / "raw" / "landing"
    ARCHIVE = BASE_DIR / "data" / "raw" / "archive"
    PROCESSED = BASE_DIR / "data" / "processed"

    ingestion = DataIngestion(landing_dir=LANDING, archive_dir=ARCHIVE, processed_dir=PROCESSED)
    ingestion.process_landing_zone()