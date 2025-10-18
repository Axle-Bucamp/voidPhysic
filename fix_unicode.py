#!/usr/bin/env python3
"""
Script to remove Unicode emoji characters from Python files for Windows compatibility.
"""

import re
import os

def remove_emojis(text):
    """Remove emoji characters and replace Greek letters with ASCII equivalents."""
    # Remove common emoji Unicode ranges
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+", flags=re.UNICODE)
    
    # Replace Greek letters with ASCII equivalents
    greek_replacements = {
        '\u03bb': 'lambda',  # λ
        '\u03c6': 'phi',     # φ
        '\u03c0': 'pi',      # π
        '\u03b1': 'alpha',   # α
        '\u03b2': 'beta',    # β
        '\u03b3': 'gamma',   # γ
        '\u0393': 'Gamma',   # Γ (capital gamma)
        '\u03b4': 'delta',   # δ
        '\u0394': 'Delta',   # Δ (capital delta)
        '\u03b5': 'epsilon', # ε
        '\u03b8': 'theta',   # θ
        '\u0398': 'Theta',   # Θ (capital theta)
        '\u03c3': 'sigma',   # σ
        '\u03a3': 'Sigma',   # Σ (capital sigma)
        '\u03c4': 'tau',     # τ
        '\u03c9': 'omega',   # ω
        '\u03a9': 'Omega',   # Ω (capital omega)
    }
    
    # Remove emojis first
    text = emoji_pattern.sub('', text)
    
    # Replace Greek letters
    for greek, ascii_equiv in greek_replacements.items():
        text = text.replace(greek, ascii_equiv)
    
    return text

def fix_file(filepath):
    """Fix a single file by removing emojis."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = remove_emojis(content)
        
        if content != fixed_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Fixed: {filepath}")
        else:
            print(f"No changes needed: {filepath}")
            
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

def main():
    """Fix all Python files in the project."""
    files_to_fix = [
        "test_math.py",
        "examples/toy_model_0d.py",
        "src/void_physic/cli.py"
    ]
    
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            fix_file(filepath)
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
