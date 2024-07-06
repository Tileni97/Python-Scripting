# Game Directory Management and Compilation Script
This Python script automates the process of managing game directories, compiling game code, and generating metadata JSON for game projects.

# Features
Directory Management: Copies game directories from a source to a target directory.
Code Compilation: Compiles game code files (e.g., .go files) if found within the copied directories.
Metadata Generation: Creates a JSON file containing metadata about the copied game directories.

# Requirements
Python 3.x
External dependencies: None (standard library only)

# Installation
Clone the repository:
git clone https://github.com/your_username/your_repository.git
Navigate to the project directory:
cd your_repository
Install Python dependencies (if any):
pip install -r requirements.txt

# Usage
Command-Line Arguments
The script accepts two required arguments:
source: Source directory containing game directories to be copied.
target: Target directory where game directories will be copied and compiled.
python get_game_data.py <source_directory> <target_directory>
### Example
python get_game_data.py C:\Games\ C:\Target\

*Replace C:\Games\ with the actual path to your source directory containing game directories, and C:\Target\ with the target directory where you want the game directories to be copied and compiled.*
