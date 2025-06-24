#!/usr/bin/env python3
"""
Convert text file with markdown file information to professional HTML format.
"""

import os
import sys
import re
import html
import json
from datetime import datetime
from pathlib import Path

def read_text_file(file_path):
    """
    Read a text file and return its contents.
    
    Args:
        file_path (str): Path to the text file
        
    Returns:
        str: Contents of the text file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        raise Exception(f"Error reading text file: {e}")

def parse_file_entry(entry_text):
    """
    Parse a single file entry from the text format.
    
    Args:
        entry_text (str): Text block for one file
        
    Returns:
        dict: Parsed file information
    """
    lines = entry_text.strip().split('\n')
    
    # Initialize file info
    file_info = {
        'filename': '',
        'size': '',
        'lines_count': '',
        'preview_lines': [],
        'remaining_lines': 0
    }
    
    # Parse file header
    in_preview_section = False
    
    for line in lines:
        # Skip separator lines
        if line.strip().startswith('--'):
            continue
            
        if line.startswith('File: '):
            file_info['filename'] = line.replace('File: ', '').strip()
        elif line.startswith('Size: '):
            # Extract size and line count
            size_info = line.replace('Size: ', '').strip()
            if 'characters' in size_info and 'lines' in size_info:
                parts = size_info.split(',')
                file_info['size'] = parts[0].strip()
                file_info['lines_count'] = parts[1].strip()
        elif line.strip().startswith('Preview (first'):
            # Start collecting preview lines
            in_preview_section = True
            continue
        elif in_preview_section and re.match(r'^\s*\d+:', line):
            # This is a preview line
            file_info['preview_lines'].append(line.strip())
        elif '... (' in line and 'more lines)' in line:
            # Extract remaining lines count
            match = re.search(r'\((\d+) more lines\)', line)
            if match:
                file_info['remaining_lines'] = int(match.group(1))
            in_preview_section = False  # End of preview section
    
    return file_info

def parse_text_content(content):
    """
    Parse the entire text content and extract all file entries.
    
    Args:
        content (str): Full text content
        
    Returns:
        list: List of parsed file information dictionaries
    """
    # Find the RESULTS section
    results_start = content.find('RESULTS')
    if results_start == -1:
        print("Could not find RESULTS section")
        return []
    
    results_content = content[results_start:]
    
    # Split by entries - look for "File: " patterns
    file_entries = []
    current_entry = ""
    
    lines = results_content.split('\n')
    for line in lines:
        if line.startswith('File: '):
            # Start of new entry, process previous if it exists
            if current_entry.strip():
                file_info = parse_file_entry(current_entry)
                if file_info['filename']:
                    file_entries.append(file_info)
            current_entry = line + '\n'
        elif current_entry:  # We're in an entry
            current_entry += line + '\n'
    
    # Process the last entry
    if current_entry.strip():
        file_info = parse_file_entry(current_entry)
        if file_info['filename']:
            file_entries.append(file_info)
    
    return file_entries

def generate_html(file_entries, title="Markdown Files Report"):
    """
    Generate professional HTML from parsed file entries.
    
    Args:
        file_entries (list): List of file information dictionaries
        title (str): HTML page title
        
    Returns:
        str: Complete HTML document
    """
    
    # CSS styling with professional blue, grey, white theme
    css = """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #2c3e50;
            line-height: 1.6;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .stats {
            background: #34495e;
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
            margin: 10px;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
            color: #3498db;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .content {
            padding: 30px;
        }
        
        .file-entry {
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            margin-bottom: 30px;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .file-entry:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        .file-header {
            background: #ecf0f1;
            padding: 20px 25px;
            border-bottom: 1px solid #bdc3c7;
        }
        
        .file-title {
            font-size: 1.3em;
            color: #2c3e50;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        .file-meta {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .meta-item {
            background: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            color: #7f8c8d;
            border: 1px solid #e0e0e0;
        }
        
        .preview-section {
            padding: 25px;
        }
        
        .preview-title {
            font-size: 1em;
            color: #34495e;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .preview-lines {
            background: #2c3e50;
            color: #ecf0f1;  
            padding: 20px;
            border-radius: 6px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.4;
            overflow-x: auto;
        }
        
        .preview-line {
            margin-bottom: 5px;
            white-space: pre-wrap;
        }
        
        .line-number {
            color: #3498db;
            margin-right: 10px;
            font-weight: bold;
        }
        
        .remaining-lines {
            margin-top: 15px;
            padding: 10px 15px;
            background: #e8f4f8;
            color: #2980b9;
            border-radius: 4px;
            font-size: 0.9em;
            border-left: 3px solid #3498db;
        }
        
        .footer {
            background: #34495e;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 8px;
            }
            
            .header {
                padding: 30px 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .stats {
                padding: 15px 20px;
            }
            
            .content {
                padding: 20px;
            }
            
            .file-meta {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
    """
    
    # Calculate statistics - with error handling
    total_files = len(file_entries)
    total_chars = 0
    total_lines = 0
    
    for entry in file_entries:
        try:
            if entry['size']:
                total_chars += int(entry['size'].split()[0])
        except (ValueError, IndexError):
            pass
        try:
            if entry['lines_count']:
                total_lines += int(entry['lines_count'].split()[0])
        except (ValueError, IndexError):
            pass
    
    # Generate HTML
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {css}
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="subtitle">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <span class="stat-number">{total_files}</span>
                <span class="stat-label">Files</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{total_chars:,}</span>
                <span class="stat-label">Characters</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{total_lines:,}</span>
                <span class="stat-label">Lines</span>
            </div>
        </div>
        
        <div class="content">
"""
    
    # Add file entries
    for entry in file_entries:
        html_doc += f"""
            <div class="file-entry">
                <div class="file-header">
                    <div class="file-title">{html.escape(entry['filename'])}</div>
                    <div class="file-meta">
                        <span class="meta-item">📄 {html.escape(entry['size'])}</span>
                        <span class="meta-item">📝 {html.escape(entry['lines_count'])}</span>
                    </div>
                </div>
                
                <div class="preview-section">
                    <div class="preview-title">Preview</div>
                    <div class="preview-lines">
"""
        
        # Add preview lines
        if entry['preview_lines']:
            for line in entry['preview_lines']:
                # Extract line number and content
                if ':' in line:
                    parts = line.split(':', 1)
                    line_num = parts[0].strip()
                    content = parts[1] if len(parts) > 1 else ''
                    # HTML escape the content to prevent issues with special characters
                    content = html.escape(content)
                    html_doc += f'                        <div class="preview-line"><span class="line-number">{line_num}:</span>{content}</div>\n'
        else:
            html_doc += '                        <div class="preview-line">No preview available</div>\n'
        
        html_doc += "                    </div>\n"
        
        # Add remaining lines info if present
        if entry['remaining_lines'] > 0:
            html_doc += f'                    <div class="remaining-lines">+ {entry["remaining_lines"]} more lines...</div>\n'
        
        html_doc += """                </div>
            </div>
"""
    
    # Close HTML
    html_doc += f"""        </div>
        
        <div class="footer">
            Report generated from markdown files analysis
        </div>
    </div>
</body>
</html>"""
    
    return html_doc

def convert_text_file_to_html(input_file, output_file=None):
    """
    Main conversion function.
    
    Args:
        input_file (str): Path to input text file
        output_file (str): Path to output HTML file (optional)
    """
    
    # Read the text file
    print(f"Reading text file: {input_file}")
    content = read_text_file(input_file)
    
    # Parse the content
    print("Parsing file entries...")
    file_entries = parse_text_content(content)
    
    if not file_entries:
        print("No file entries found in the text file.")
        return
    
    print(f"Found {len(file_entries)} file entries")
    for entry in file_entries:
        print(f"  - {entry['filename']}: {len(entry['preview_lines'])} preview lines")
    
    # Generate HTML
    print("Generating HTML...")
    html_content = generate_html(file_entries, "Markdown Files Report")
    
    # Determine output file name
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.with_suffix('.html')
    
    # Write HTML file
    print(f"Writing HTML file: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Successfully converted to HTML: {output_file}")
    return output_file

def convert_dict_to_html(file_contents, output_file=None):
    """
    Main conversion function.
    
    Args:
        dictionary of str: Strings to process
        output_file (str): Path to output HTML file (optional)
    """
    
    # Read the text file
    print(f"Reading file contents...")
    content = json.dumps(file_contents)
    print(content)
    
    # Parse the content
    print("Parsing file entries...")
    file_entries = parse_text_content(content)
    
    if not file_entries:
        print("No file entries found in the text file.")
        return
    
    print(f"Found {len(file_entries)} file entries")
    for entry in file_entries:
        print(f"  - {entry['filename']}: {len(entry['preview_lines'])} preview lines")
    
    # Generate HTML
    print("Generating HTML...")
    html_content = generate_html(file_entries, "Markdown Files Report")
    
    # Determine output file name
    if output_file is None:
        output_file = 'index.html'
    
    # Write HTML file
    print(f"Writing HTML file: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Successfully converted to HTML: {output_file}")
    return output_file

