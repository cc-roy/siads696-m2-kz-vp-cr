#!/usr/bin/env python3

import sys
import os
import numpy as np
import pandas as pd
import pickle
import warnings

warnings.filterwarnings('ignore')

def convert_pickle_to_parquet(pickle_file, parquet_file=None):
    """
    Convert a pickle file to parquet format using a custom unpickler
    that handles older numpy versions.
    """
    if parquet_file is None:
        parquet_file = os.path.splitext(pickle_file)[0] + '.parquet'
    
    print(f"Converting {pickle_file} to {parquet_file}...")
    
    # Try multiple approaches to load the pickle file
    try:
        # Approach 1: Use a modified environment to load the pickle
        # This creates a custom unpickler that can handle older numpy structures
        class CustomUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                # Handle numpy._core.numeric module not found
                if module == 'numpy._core.numeric':
                    module = 'numpy.core.numeric'
                # Handle other potential module path changes
                elif module.startswith('numpy.'):
                    try:
                        return super().find_class(module, name)
                    except ModuleNotFoundError:
                        # Try alternative numpy paths
                        alt_module = module.replace('numpy._', 'numpy.')
                        try:
                            return super().find_class(alt_module, name)
                        except:
                            pass
                return super().find_class(module, name)
        
        # Try with custom unpickler
        with open(pickle_file, 'rb') as f:
            df = CustomUnpickler(f).load()
        
    except Exception as e:
        print(f"Custom unpickler failed: {e}")
        
        try:
            # Approach 2: Try with latin1 encoding (helps with Python 2/3 compatibility)
            with open(pickle_file, 'rb') as f:
                df = pickle.load(f, encoding='latin1')
        except Exception as e:
            print(f"Latin1 encoding failed: {e}")
            
            try:
                # Approach 3: Try pandas read_pickle with fixed protocol
                df = pd.read_pickle(pickle_file)
            except Exception as e:
                print(f"Pandas read_pickle failed: {e}")
                print("All approaches failed. Cannot convert the file.")
                return False
    
    # Save as parquet
    try:
        df.to_parquet(parquet_file)
        print(f"Successfully converted to {parquet_file}")
        return True
    except Exception as e:
        print(f"Error saving to parquet: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_pickle_to_parquet.py <pickle_file> [parquet_file]")
        sys.exit(1)
    
    pickle_file = sys.argv[1]
    parquet_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_pickle_to_parquet(pickle_file, parquet_file)
    sys.exit(0 if success else 1) 