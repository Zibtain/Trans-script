import argparse
import glob
import logging
import os
import re

def setup_logging():
    """Set up logging to both file and console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('transcript_cleaning.log'),
            logging.StreamHandler()
        ]
    )

def detect_transcript_format(text):
    """Detect the transcript format based on timestamp patterns."""
    patterns = {
        'srt': r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}',
        'vtt': r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}',
        'simple': r'\d{1,2}:\d{2}(,\d{1,3})? --> \d{1,2}:\d{2}(,\d{1,3})?'
    }
    
    for format_name, pattern in patterns.items():
        if re.search(pattern, text):
            logging.info(f"Detected transcript format: {format_name}")
            return format_name
    logging.warning("No known format detected, defaulting to SRT")
    return 'srt'

def clean_transcripts(text, format_type='srt'):
    """Clean transcript text by removing timestamps, line numbers, and empty lines."""
    logging.info("Starting transcript cleaning")
    original_lines = len(text.split('\n'))
    
    # Define timestamp patterns for different formats
    timestamp_patterns = {
        'srt': r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}',
        'vtt': r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}',
        'simple': r'\d{1,2}:\d{2}(,\d{1,3})? --> \d{1,2}:\d{2}(,\d{1,3})?'
    }
    
    # Use detected format or specified format
    pattern = timestamp_patterns.get(format_type, timestamp_patterns['srt'])
    
    # Remove timestamps
    text = re.sub(pattern, '', text)
    
    # Remove line numbers (numbers at the start of a line)
    text = re.sub(r'^\d+\s*$\n', '', text, flags=re.MULTILINE)
    
    # Remove empty lines
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
    
    cleaned_lines = len(text.split('\n'))
    logging.info(f"Removed {original_lines - cleaned_lines} lines")
    return text

def process_file(input_path, output_path, format_type):
    """Process a single transcript file."""
    logging.info(f"Processing file: {input_path}")
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            document = file.read()
        
        # Auto-detect format if not specified
        if format_type == 'auto':
            format_type = detect_transcript_format(document)
        
        cleaned_document = clean_transcripts(document, format_type)
        
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(cleaned_document)
        logging.info(f"Cleaned transcript saved to {output_path}")
    
    except FileNotFoundError:
        logging.error(f"File not found: {input_path}")
        print(f"Error: The file '{input_path}' was not found.")
    except PermissionError:
        logging.error(f"Permission denied: {input_path}")
        print(f"Error: Permission denied when accessing the file.")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"An unexpected error occurred: {e}")

def main():
    """Main function with CLI and interactive modes."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Clean transcript files by removing timestamps and line numbers.")
    parser.add_argument("input", help="Path to the input file or directory")
    parser.add_argument("-o", "--output", default=None, help="Output file or directory (default: cleaned_<input>)")
    parser.add_argument("--format", choices=['srt', 'vtt', 'simple', 'auto'], default='auto',
                        help="Transcript format (default: auto-detect)")
    
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output
    format_type = args.format
    
    if os.path.isfile(input_path):
        if output_path is None:
            output_path = f"cleaned_{os.path.basename(input_path)}"
        process_file(input_path, output_path, format_type)
    
    elif os.path.isdir(input_path):
        output_dir = output_path or os.getcwd()
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all .srt and .vtt files
        transcript_files = glob.glob(os.path.join(input_path, "*.srt")) + glob.glob(os.path.join(input_path, "*.vtt"))
        
        if not transcript_files:
            logging.warning(f"No transcript files (.srt or .vtt) found in directory: {input_path}")
            print("No transcript files (.srt or .vtt) found in the directory.")
            return
        
        for file_path in transcript_files:
            base_name = os.path.basename(file_path)
            output_file = os.path.join(output_dir, f"cleaned_{base_name}")
            process_file(file_path, output_file, format_type)
    
    else:
        logging.error(f"Invalid input path: {input_path}")
        print(f"Error: '{input_path}' is not a valid file or directory.")

if __name__ == "__main__":
    main()