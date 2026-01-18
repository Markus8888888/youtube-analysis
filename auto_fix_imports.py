#!/usr/bin/env python3
"""
Automatically fix import paths in all Python files
Run this from your project root
"""

import os
import re

def fix_imports_in_file(filepath):
    """Fix imports in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Define replacements based on the file location
        if 'src/ai_brain/' in filepath:
            # Fix imports within ai_brain package
            replacements = [
                ('from gemini_client import', 'from src.ai_brain.gemini_client import'),
                ('from chat_manager import', 'from src.ai_brain.chat_manager import'),
                ('from prompts import', 'from src.ai_brain.prompts import'),
                ('from error_handlers import', 'from src.ai_brain.error_handlers import'),
                ('from cache import', 'from src.ai_brain.cache import'),
                ('from logger import', 'from src.ai_brain.logger import'),
            ]
        elif 'src/data_miner/' in filepath:
            # Fix imports within data_miner package
            replacements = [
                ('from .youtube_link_processor import', 'from src.data_miner.youtube_link_processor import'),
                ('from .youtube_data_processor import', 'from src.data_miner.youtube_data_processor import'),
                ('from .youtube_api import', 'from src.data_miner.youtube_api import'),
                ('from .data_cleaner import', 'from src.data_miner.data_cleaner import'),
            ]
        elif 'src/frontend/' in filepath:
            # Fix imports within frontend package
            replacements = [
                ('from visualizations import', 'from src.frontend.visualizations import'),
            ]
        elif 'src/backend/' in filepath:
            # Fix imports within backend package
            replacements = [
                ('from data_miner.youtube_api import', 'from src.data_miner.youtube_api import'),
                ('from ai_brain.brain import', 'from src.ai_brain.brain import'),
            ]
        else:
            return False
        
        # Apply replacements
        for old, new in replacements:
            content = content.replace(old, new)
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {filepath}")
            return True
        else:
            print(f"⏭️  No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        return False

def find_python_files(directory):
    """Find all Python files in directory"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                python_files.append(os.path.join(root, file))
    
    return python_files

def main():
    print("🔧 Auto-fixing import paths...\n")
    
    # Find all Python files in src/
    if not os.path.exists('src'):
        print("❌ Error: 'src' directory not found. Are you in the project root?")
        return
    
    python_files = find_python_files('src')
    
    if not python_files:
        print("⚠️  No Python files found in src/")
        return
    
    print(f"Found {len(python_files)} Python files to check\n")
    
    fixed_count = 0
    for filepath in python_files:
        if fix_imports_in_file(filepath):
            fixed_count += 1
    
    print(f"\n✨ Done! Fixed {fixed_count} file(s)")
    print("\nNow try running: streamlit run app.py")

if __name__ == "__main__":
    main()