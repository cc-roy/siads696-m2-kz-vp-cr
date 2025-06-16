#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile

def create_conversion_script():
    """Create a temporary script that will be run in the virtual environment."""
    script = """
import os
import sys
import pandas as pd
import numpy as np

pickle_file = sys.argv[1]
parquet_file = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(pickle_file)[0] + '.parquet'

print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")
print(f"Converting {pickle_file} to {parquet_file}...")

try:
    # Try to load the pickle file
    df = pd.read_pickle(pickle_file)
    
    # Save as parquet
    df.to_parquet(parquet_file)
    print(f"Successfully converted to {parquet_file}")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
"""
    fd, path = tempfile.mkstemp(suffix='.py', text=True)
    with os.fdopen(fd, 'w') as f:
        f.write(script)
    return path

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_with_older_numpy.py <pickle_file> [parquet_file]")
        sys.exit(1)
    
    pickle_file = sys.argv[1]
    parquet_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(pickle_file):
        print(f"Error: File {pickle_file} does not exist.")
        sys.exit(1)
    
    if parquet_file is None:
        parquet_file = os.path.splitext(pickle_file)[0] + '.parquet'
    
    # Create a temporary script for the conversion
    script_path = create_conversion_script()
    
    try:
        # Create and set up virtual environment
        print("Creating virtual environment with older numpy version...")
        venv_dir = tempfile.mkdtemp(prefix='numpy_compat_venv_')
        
        # Create the virtual environment
        subprocess.run([sys.executable, '-m', 'venv', venv_dir], check=True)
        
        # Determine the pip path in the virtual environment
        if sys.platform == 'win32':
            pip_path = os.path.join(venv_dir, 'Scripts', 'pip')
        else:
            pip_path = os.path.join(venv_dir, 'bin', 'pip')
        
        # Install older versions of numpy and pandas
        print("Installing older versions of numpy and pandas...")
        subprocess.run([pip_path, 'install', 'numpy==1.23.5'], check=True)
        subprocess.run([pip_path, 'install', 'pandas==1.5.3'], check=True)
        subprocess.run([pip_path, 'install', 'pyarrow'], check=True)
        
        # Determine the python path in the virtual environment
        if sys.platform == 'win32':
            python_path = os.path.join(venv_dir, 'Scripts', 'python')
        else:
            python_path = os.path.join(venv_dir, 'bin', 'python')
        
        # Run the conversion script in the virtual environment
        print("Running conversion in virtual environment...")
        subprocess.run([python_path, script_path, pickle_file, parquet_file], check=True)
        
        print(f"Conversion complete. Output file: {parquet_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)
    finally:
        # Clean up
        if os.path.exists(script_path):
            os.unlink(script_path)
        # Note: We're not removing the venv_dir to avoid issues with file locks
        # You may want to clean it up manually later

if __name__ == "__main__":
    main() 