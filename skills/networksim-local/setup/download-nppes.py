#!/usr/bin/env python3
"""
NetworkSim-Local: NPPES Data Downloader

Downloads the NPPES NPI Registry data from CMS.

Usage:
    python download-nppes.py [--output-dir PATH] [--version {1,2}]

Example:
    python download-nppes.py --output-dir ../data/nppes
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.error

# Try to import optional progress bar
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


# CMS NPPES download base URL
NPPES_BASE_URL = "https://download.cms.gov/nppes"

# Month names for URL construction
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


class DownloadProgressBar:
    """Progress bar for urllib downloads."""
    
    def __init__(self, total_size: int, desc: str = "Downloading"):
        self.total_size = total_size
        self.desc = desc
        self.downloaded = 0
        if HAS_TQDM:
            self.pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc=desc)
        else:
            self.last_percent = -1
    
    def update(self, block_size: int):
        self.downloaded += block_size
        if HAS_TQDM:
            self.pbar.update(block_size)
        else:
            percent = int(100 * self.downloaded / self.total_size) if self.total_size > 0 else 0
            if percent != self.last_percent and percent % 10 == 0:
                print(f"  {percent}% complete...")
                self.last_percent = percent
    
    def close(self):
        if HAS_TQDM:
            self.pbar.close()


def get_nppes_url(year: int, month: int, version: int = 1) -> str:
    """Construct NPPES download URL for given year/month."""
    month_name = MONTHS[month - 1]
    
    if version == 2:
        filename = f"NPPES_Data_Dissemination_{month_name}_{year}_V2.zip"
    else:
        filename = f"NPPES_Data_Dissemination_{month_name}_{year}.zip"
    
    return f"{NPPES_BASE_URL}/{filename}"


def check_url_exists(url: str) -> tuple[bool, int]:
    """Check if URL exists and get file size."""
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=30) as response:
            size = int(response.headers.get('Content-Length', 0))
            return True, size
    except urllib.error.HTTPError:
        return False, 0
    except Exception as e:
        print(f"Warning: Could not check URL: {e}")
        return False, 0


def find_latest_nppes(version: int = 1) -> tuple[str, int, int]:
    """Find the most recent available NPPES file."""
    now = datetime.now()
    
    # Try current month, then go back up to 3 months
    for months_back in range(4):
        year = now.year
        month = now.month - months_back
        
        # Handle year rollover
        if month <= 0:
            month += 12
            year -= 1
        
        url = get_nppes_url(year, month, version)
        exists, size = check_url_exists(url)
        
        if exists:
            return url, year, month
    
    return None, None, None


def download_file(url: str, output_path: Path) -> bool:
    """Download file with progress bar."""
    try:
        # Get file size
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=30) as response:
            total_size = int(response.headers.get('Content-Length', 0))
        
        print(f"Downloading: {url}")
        print(f"Size: {total_size / (1024*1024):.1f} MB")
        print(f"Output: {output_path}")
        
        # Download with progress
        progress = DownloadProgressBar(total_size, "Downloading")
        
        def reporthook(block_num, block_size, total_size):
            progress.update(block_size)
        
        urllib.request.urlretrieve(url, output_path, reporthook)
        progress.close()
        
        print(f"\nDownload complete!")
        return True
        
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def extract_zip(zip_path: Path, output_dir: Path) -> list[Path]:
    """Extract ZIP file and return list of extracted files."""
    print(f"\nExtracting: {zip_path}")
    
    extracted = []
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # List contents
        print(f"Contents:")
        for info in zf.infolist():
            size_mb = info.file_size / (1024 * 1024)
            print(f"  {info.filename} ({size_mb:.1f} MB)")
        
        # Extract
        print(f"\nExtracting to: {output_dir}")
        zf.extractall(output_dir)
        
        for info in zf.infolist():
            extracted.append(output_dir / info.filename)
    
    print(f"Extraction complete!")
    return extracted


def main():
    parser = argparse.ArgumentParser(
        description='Download NPPES NPI Registry data from CMS'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help='Output directory (default: ../data/nppes relative to script)'
    )
    parser.add_argument(
        '--version',
        type=int,
        choices=[1, 2],
        default=1,
        help='NPPES file version (1=original, 2=extended fields)'
    )
    parser.add_argument(
        '--year',
        type=int,
        default=None,
        help='Specific year to download'
    )
    parser.add_argument(
        '--month',
        type=int,
        choices=range(1, 13),
        default=None,
        help='Specific month to download (1-12)'
    )
    parser.add_argument(
        '--keep-zip',
        action='store_true',
        help='Keep the ZIP file after extraction'
    )
    parser.add_argument(
        '--no-extract',
        action='store_true',
        help='Download only, do not extract'
    )
    
    args = parser.parse_args()
    
    # Determine output directory
    script_dir = Path(__file__).parent
    output_dir = args.output_dir or (script_dir.parent / 'data' / 'nppes')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("NetworkSim-Local: NPPES Data Downloader")
    print("=" * 60)
    
    # Find or construct URL
    if args.year and args.month:
        url = get_nppes_url(args.year, args.month, args.version)
        year, month = args.year, args.month
        exists, _ = check_url_exists(url)
        if not exists:
            print(f"ERROR: File not found for {MONTHS[month-1]} {year}")
            sys.exit(1)
    else:
        print(f"\nSearching for latest NPPES file (version {args.version})...")
        url, year, month = find_latest_nppes(args.version)
        
        if not url:
            print("ERROR: Could not find any recent NPPES files.")
            print("Try specifying --year and --month manually.")
            sys.exit(1)
        
        print(f"Found: {MONTHS[month-1]} {year}")
    
    # Download
    zip_filename = url.split('/')[-1]
    zip_path = output_dir / zip_filename
    
    print()
    if not download_file(url, zip_path):
        sys.exit(1)
    
    # Extract
    if not args.no_extract:
        extracted = extract_zip(zip_path, output_dir)
        
        # Find main data file
        main_file = None
        for f in extracted:
            if f.name.startswith('npidata_pfile_') and f.name.endswith('.csv'):
                main_file = f
                break
        
        if main_file:
            print(f"\nMain data file: {main_file}")
            print(f"Size: {main_file.stat().st_size / (1024*1024*1024):.2f} GB")
        
        # Clean up ZIP
        if not args.keep_zip:
            print(f"\nRemoving ZIP file...")
            zip_path.unlink()
    
    print("\n" + "=" * 60)
    print("Download complete!")
    print(f"Output directory: {output_dir}")
    print("=" * 60)
    
    # Print next steps
    print("\nNext steps:")
    print("  1. Run: python build-database.py")
    print("  2. Verify: python validate-db.py")


if __name__ == '__main__':
    main()
