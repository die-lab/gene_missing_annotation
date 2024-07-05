import os
import sys
import numpy as np

def find_outlier_files(directory):
    # Get the list of files and their sizes
    files = [(f, os.path.getsize(os.path.join(directory, f))) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        print("No files found in the directory.")
        return

    # Calculate mean and standard deviation
    sizes = np.array([size for _, size in files])
    mean_size = np.mean(sizes)
    std_dev_size = np.std(sizes)

    ### Determine outliers (files with size more than 2 standard deviations from the mean)
    threshold = 2 * std_dev_size
    #outliers = [(file, size) for file, size in files if size - mean_size > threshold]
    greater_outliers = [(file, size) for file, size in files if size - mean_size > threshold]
    
    ### Print out the results
    #print(f"Mean file size: {mean_size} bytes")
    #print(f"Standard deviation of file sizes: {std_dev_size} bytes")
    #print("\nOutlier files:")
    for file, size in greater_outliers:
        print(f"{file}: {size} bytes (Deviation: {abs(size - mean_size)} bytes)")

# Usage
directory_path = sys.argv[1]
find_outlier_files(directory_path)
