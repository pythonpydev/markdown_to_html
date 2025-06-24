"""
Script to import and read markdown files.
"""

import sys
import os
from pathlib import Path

def get_path():
    # Check if a directory path was provided as command line argument
    if len(sys.argv) > 2:
        directory = sys.argv[1]
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist.")
            return
        if not os.path.isdir(directory):
            print(f"Error: '{directory}' is not a directory.")
            return
    else:
        directory = '.'
        print("No directory specified, using current directory.")
    return directory

def print_content(file_contents, md_files):
    # Display results
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")
    
    successful_reads = 0
    total_characters = 0
    total_lines = 0
    
    for file_path, content in file_contents.items():
        if content is not None:
            successful_reads += 1
            char_count = len(content)
            line_count = len(content.splitlines())
            total_characters += char_count
            total_lines += line_count
            
            print(f"\n{'-'*50}")
            print(f"File: {file_path}")
            print(f"Size: {char_count} characters, {line_count} lines")
            print(f"{'-'*50}")
            
            # Display first few lines as preview
            lines = content.splitlines()
            preview_lines = min(5, len(lines))
            
            print("Preview (first 5 lines):")
            for i in range(preview_lines):
                print(f"  {i+1}: {lines[i]}")
            
            if len(lines) > preview_lines:
                print(f"  ... ({len(lines) - preview_lines} more lines)")
            
            # Optionally display full content (uncomment if needed)
            # print("\nFull Content:")
            # print(content)
        else:
            print(f"\n✗ Failed to read: {file_path}")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total files found: {len(md_files)}")
    print(f"Successfully read: {successful_reads}")
    print(f"Failed to read: {len(md_files) - successful_reads}")
    print(f"Total characters: {total_characters:,}")
    print(f"Total lines: {total_lines:,}")

def read_markdown_file(file_path):
    """
    Read a markdown file and return its contents.
    
    Args:
        file_path (str or Path): Path to the markdown file
        
    Returns:
        str: Contents of the markdown file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If unable to read the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Markdown file not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied reading file: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading markdown file: {e}")

def find_markdown_files(directory='.'):
    """
    Find all markdown files in a directory.
    
    Args:
        directory (str): Directory to search (default: current directory)
        
    Returns:
        list: List of Path objects for markdown files
    """
    directory = Path(directory)
    md_files = list(directory.glob('*.md'))
    return md_files

def read_all_markdown_files(directory='.'):
    """
    Read all markdown files in a directory.
    
    Args:
        directory (str): Directory to search (default: current directory)
        
    Returns:
        dict: Dictionary with file paths as keys and content as values
    """
    md_files = find_markdown_files(directory)
    file_contents = {}
    
    for file_path in md_files:
        try:
            content = read_markdown_file(file_path)
            file_contents[str(file_path)] = content
            print(f"✓ Successfully read: {file_path}")
        except Exception as e:
            print(f"✗ Error reading {file_path}: {e}")
            file_contents[str(file_path)] = None
    
    return file_contents