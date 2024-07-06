import os
import json
import shutil
from subprocess import PIPE, run
import argparse

# Constants for the script
GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]  # Example command for compiling Go code

def find_all_game_paths(source):
    """Find all directories containing 'game' in their name."""
    game_paths = []

    try:
        # Walk through the directory tree starting from 'source'
        for root, dirs, files in os.walk(source):
            for directory in dirs:
                # Check if the directory name contains 'game' (case-insensitive)
                if GAME_DIR_PATTERN in directory.lower():
                    path = os.path.join(root, directory)
                    game_paths.append(path)
    except OSError as e:
        print(f"Error finding game directories: {e}")
        # Handle or raise the exception as needed

    return game_paths

def get_names_from_paths(paths, to_strip):
    """Strip '_game' from directory names."""
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        # Remove '_game' from the directory name
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)
    return new_names

def create_dir(path):
    """Create directory if it doesn't exist."""
    try:
        # Check if the directory already exists; create it if not
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as e:
        print(f"Error creating directory '{path}': {e}")
        # Handle or raise the exception as needed

def copy_and_overwrite(source, dest):
    """Copy directories and overwrite if exists."""
    try:
        # If the destination directory already exists, remove it
        if os.path.exists(dest):
            shutil.rmtree(dest)
        # Copy the source directory to the destination
        shutil.copytree(source, dest)
    except (shutil.Error, OSError) as e:
        print(f"Error copying '{source}' to '{dest}': {e}")
        # Handle or raise the exception as needed

def make_json_metadata_file(path, game_dirs):
    """Create JSON metadata file."""
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }

    try:
        # Write the metadata dictionary as JSON to the specified file path
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error writing JSON metadata file '{path}': {e}")
        # Handle or raise the exception as needed

def compile_game_code(path):
    """Compile game code if exists."""
    code_file_name = None
    try:
        # Traverse the directory to find a file with the specified extension
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(GAME_CODE_EXTENSION):
                    code_file_name = file
                    break

        if code_file_name:
            # Build the compile command with the found code file name
            command = GAME_COMPILE_COMMAND + [code_file_name]
            # Execute the compile command in the specified path
            run_command(command, path)
        else:
            print(f"No code file with extension '{GAME_CODE_EXTENSION}' found in '{path}'. Skipping compilation.")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Error compiling code in '{path}': {e}")
        # Handle or raise the exception as needed

def run_command(command, path):
    """Run a command in a specified path."""
    cwd = os.getcwd()
    os.chdir(path)

    try:
        # Change directory to the specified path and run the command
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, check=True)
        print(f"Compile result in '{path}': {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{' '.join(command)}' in '{path}': {e.stderr}")
    finally:
        # Restore the current working directory
        os.chdir(cwd)

def main(source, target):
    """Main function to execute the script."""
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    # Find all game directories in the source path
    game_paths = find_all_game_paths(source_path)

    # Strip '_game' from directory names to create new names for target directories
    new_game_dirs = get_names_from_paths(game_paths, "_game")

    # Ensure the target directory exists; create it if it doesn't
    create_dir(target_path)

    # Copy each game directory to the target directory and compile game code if exists
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)

    # Create metadata.json file in the target directory
    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Copy game directories, compile game code, and generate metadata JSON.")
    parser.add_argument("source", help="Source directory containing game directories")
    parser.add_argument("target", help="Target directory where game directories will be copied")
    args = parser.parse_args()

    # Call main function with parsed arguments
    main(args.source, args.target)
