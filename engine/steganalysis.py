import cv2
import numpy as np
from scipy.stats import chisquare

def check_stego(image_path):
    """
    Performs a Chi-Square statistical test on the Least Significant Bits (LSB)
    of an image to detect potential steganography.
    Optimized for background service execution.
    """
    try:
        if not os.path.exists(image_path):
            return False
            
        img = cv2.imread(image_path)
        if img is None:
            return False
            
        # Convert to grayscale for initial statistical check
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        pixels = gray.flatten()
        
        # We only care about the distribution of even and odd pixel values (LSB)
        # In a natural image, 2i and 2i+1 should have similar counts
        counts = np.bincount(pixels, minlength=256)
        
        observed = []
        expected = []
        
        for i in range(0, 256, 2):
            count_2i = counts[i]
            count_2i_plus_1 = counts[i+1]
            
            pair_sum = count_2i + count_2i_plus_1
            mean = pair_sum / 2.0
            
            if mean > 10: # Only check pairs with enough data for statistical significance
                observed.extend([count_2i, count_2i_plus_1])
                expected.extend([mean, mean])
        
        if len(observed) < 10:
            return False
            
        _, p_value = chisquare(observed, f_exp=expected)
        
        # If p-value is very high, it means the even/odd distribution is 
        # suspiciously uniform (characteristic of LSB steganography)
        return p_value > 0.95
        
    except Exception as e:
        print(f"Error analyzing image {image_path}: {e}")
        return False

if __name__ == "__main__":
    import sys
    import os
    if len(sys.argv) > 1:
        res = check_stego(sys.argv[1])
        print(f"Stego Detected: {res}")
