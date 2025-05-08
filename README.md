# Trans_scripts 
A Python script designed to clean lecture transcripts by removing timestamps, line numbers, and empty lines, making them easier to read and study. Originally created to process Panopto transcripts for personal study, this tool has been enhanced to support multiple transcript formats (SRT, VTT, and simple), with robust error handling, logging, and customizable output options. Perfect for students, researchers, or anyone looking to streamline transcript-based learning.

Features

Timestamp Removal: Strips out timestamps in SRT, VTT, or simple formats.
Line Number Removal: Removes standalone line numbers while preserving numbers in the transcript text.
Empty Line Cleanup: Eliminates blank lines for a cleaner output.
Format Auto-Detection: Automatically detects transcript format (SRT, VTT, or simple) or allows manual specification.
Error Handling: Gracefully handles file not found, permission issues, and other errors with user-friendly messages.
Logging: Records processing details to a log file (transcript_cleaning.log) and console for transparency.
Flexible Input/Output: Processes single files or entire directories, with customizable output file or directory names.
UTF-8 Encoding: Ensures consistent handling of text files across platforms.

Installation

Ensure Python 3.6+ is installed on your system.
Clone or download this repository.
Install required dependencies:pip install -r requirements.txt

Note: The script uses only standard Python libraries (argparse, glob, logging, os, re), so no additional packages are required unless specified.

Usage
The script can be run in two modes: command-line interface (CLI) or interactive.
CLI Mode
Run the script from the terminal with the following command:
python Trans-scripts.py <input_path> [-o <output_path>] [--format <format>]


<input_path>: Path to a single transcript file (e.g., lecture.srt) or a directory containing .srt or .vtt files.
-o, --output (optional): Specify the output file or directory. Defaults to cleaned_<input_filename> for files or the current directory for directories.
--format (optional): Specify the transcript format (srt, vtt, simple, or auto). Defaults to auto.

Examples:

Process a single file:python Trans-scripts.py lecture.srt -o cleaned_lecture.txt

Process all .srt and .vtt files in a directory:python Trans-scripts.py transcripts/ -o cleaned_transcripts/

Auto-detect format:python Trans-scripts.py lecture.vtt --format auto

Interactive Mode
Run the script without arguments to prompt for input:
python Trans-scripts.py

Enter the file or directory path when prompted, and optionally specify the output path and format.
Example Input/Output
Input (lecture.srt):
1
00:00:01,000 --> 00:00:03,000
Welcome to the lecture.

2
00:00:04,000 --> 00:00:06,000
Today, we'll discuss Trans-scripts.

Output (cleaned_lecture.txt):
Welcome to the lecture.
Today, we'll discuss Trans-scripts.

Logging
The script generates a log file (transcript_cleaning.log) in the working directory, recording:

Detected transcript format
Number of lines removed
File processing status
Any errors encountered

Contributing
Contributions are welcome! Feel free to submit issues or pull requests to enhance functionality or fix bugs. Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m "Add new feature").
Push to the branch (git push origin feature-branch).
Open a pull request.

For questions or feedback, reach out via LinkedIn or open an issue on this repository.
Happy studying!
