#!/usr/bin/env python3
import os
import sys
import read_markdown as rm
import md_to_html as mth

def main():
    """Main function to read all markdown files in a directory."""

    directory = rm.get_path() 
    print(f"\nSearching for markdown files in: {os.path.abspath(directory)}")
    
    # Find all markdown files
    md_files = rm.find_markdown_files(directory)
    
    if not md_files:
        print("No markdown files found in the specified directory.")
        print("Usage: python script.py <directory_path>")
        return
    
    print(f"Found {len(md_files)} markdown file(s):")
    for file_path in md_files:
        print(f"  - {file_path}")
    
    print(f"\n{'='*60}")
    print("Reading all markdown files...")
    print(f"{'='*60}")

    # Read all markdown files
    file_contents = rm.read_all_markdown_files(directory)
    
    rm.print_content(file_contents, md_files)
    
    # Return the file contents for potential use in other scripts
    # return file_contents

    """Convert to HTML."""

    print("Converting to HTML...")

    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path> [output_html_file]")
        print("Example: python script.py report.txt report.html")
        return
    
    input_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return
    
    try:
        result_file = mth.convert_text_file_to_html(input_file, output_file)
        print(f"\n🎉 Conversion complete! Open {result_file} in your browser to view the report.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()