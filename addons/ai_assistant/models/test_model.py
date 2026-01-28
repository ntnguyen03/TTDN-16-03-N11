# Tạo một file test_model.py riêng để chạy thử
import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyD9bfFXg2hH--ePCYxzkSqnZXLKQJC3zVw")

print("Danh sách các model hiện có:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)