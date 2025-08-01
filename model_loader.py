"""
Memory-efficient model loader for the Movie Recommender System.
This script optimizes the model files to reduce memory usage on Render.
"""

import os
import pickle
import pandas as pd
import numpy as np
import gc

def optimize_movies_file():
    """
    Optimize the movies.pkl file to reduce memory usage.
    Only keeps essential columns and converts to more memory-efficient types.
    """
    if not os.path.exists('artifacts/movies.pkl'):
        print("Error: movies.pkl file not found in artifacts directory")
        return False
    
    try:
        print("Loading movies.pkl file...")
        movies = pickle.load(open('artifacts/movies.pkl', 'rb'))
        
        print(f"Original movies dataframe shape: {movies.shape}")
        print(f"Original movies dataframe memory usage: {movies.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB")
        
        # Keep only essential columns
        essential_columns = ['id', 'title']
        if set(essential_columns).issubset(movies.columns):
            movies = movies[essential_columns]
        
        # Convert to more memory-efficient types
        if 'id' in movies.columns:
            movies['id'] = pd.to_numeric(movies['id'], errors='coerce')
        
        # Reset index
        movies = movies.reset_index(drop=True)
        
        print(f"Optimized movies dataframe shape: {movies.shape}")
        print(f"Optimized movies dataframe memory usage: {movies.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB")
        
        # Save optimized file
        with open('artifacts/movies_optimized.pkl', 'wb') as f:
            pickle.dump(movies, f, protocol=4)
        
        print("Successfully created optimized movies file: artifacts/movies_optimized.pkl")
        
        # Force garbage collection
        del movies
        gc.collect()
        
        return True
    
    except Exception as e:
        print(f"Error optimizing movies file: {e}")
        return False

def optimize_neighbors_file():
    """
    Optimize the all_neighbors.pkl file to reduce memory usage.
    Limits the number of neighbors to 30 per movie.
    """
    if not os.path.exists('artifacts/all_neighbors.pkl'):
        print("Error: all_neighbors.pkl file not found in artifacts directory")
        return False
    
    try:
        print("Loading all_neighbors.pkl file...")
        neighbors = pickle.load(open('artifacts/all_neighbors.pkl', 'rb'))
        
        print(f"Original neighbors array shape: {neighbors.shape if hasattr(neighbors, 'shape') else 'unknown'}")
        
        # Limit to 30 neighbors per movie to save memory
        optimized_neighbors = []
        for movie_neighbors in neighbors:
            # Keep only the first 31 neighbors (including the movie itself)
            optimized_neighbors.append(movie_neighbors[:31])
        
        # Convert to numpy array if it's not already
        optimized_neighbors = np.array(optimized_neighbors)
        
        print(f"Optimized neighbors array shape: {optimized_neighbors.shape}")
        
        # Save optimized file
        with open('artifacts/neighbors_optimized.pkl', 'wb') as f:
            pickle.dump(optimized_neighbors, f, protocol=4)
        
        print("Successfully created optimized neighbors file: artifacts/neighbors_optimized.pkl")
        
        # Force garbage collection
        del neighbors
        del optimized_neighbors
        gc.collect()
        
        return True
    
    except Exception as e:
        print(f"Error optimizing neighbors file: {e}")
        return False

def rename_optimized_files():
    """
    Rename optimized files to replace the original files.
    """
    try:
        if os.path.exists('artifacts/movies_optimized.pkl'):
            if os.path.exists('artifacts/movies.pkl'):
                os.rename('artifacts/movies.pkl', 'artifacts/movies_original.pkl')
            os.rename('artifacts/movies_optimized.pkl', 'artifacts/movies.pkl')
            print("Renamed movies_optimized.pkl to movies.pkl")
        
        if os.path.exists('artifacts/neighbors_optimized.pkl'):
            if os.path.exists('artifacts/all_neighbors.pkl'):
                os.rename('artifacts/all_neighbors.pkl', 'artifacts/all_neighbors_original.pkl')
            os.rename('artifacts/neighbors_optimized.pkl', 'artifacts/all_neighbors.pkl')
            print("Renamed neighbors_optimized.pkl to all_neighbors.pkl")
        
        return True
    
    except Exception as e:
        print(f"Error renaming optimized files: {e}")
        return False

if __name__ == "__main__":
    print("Starting model optimization process...")
    
    # Create artifacts directory if it doesn't exist
    os.makedirs('artifacts', exist_ok=True)
    
    # Optimize movies file
    movies_optimized = optimize_movies_file()
    
    # Optimize neighbors file
    neighbors_optimized = optimize_neighbors_file()
    
    # Rename optimized files if both optimizations were successful
    if movies_optimized and neighbors_optimized:
        rename_optimized_files()
        print("Model optimization completed successfully!")
    else:
        print("Model optimization completed with errors. Check the logs for details.")