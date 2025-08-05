#!/usr/bin/env python3
"""
Quick script to regenerate all sample data
Usage: python run_data_generator.py
"""

import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate_sample_data import generate_complete_dataset

if __name__ == "__main__":
    print("🌾 Malaysian Smart Farm Data Generator")
    print("=" * 40)
    
    try:
        dataset = generate_complete_dataset()
        print("\n✅ All data generated successfully!")
        print("\nTo start the system:")
        print("1. Backend: python main.py")
        print("2. Frontend: npm start")
        
    except Exception as e:
        print(f"\n❌ Error generating data: {e}")
        sys.exit(1)