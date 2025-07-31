import os
import shutil

file = input("file path: ").strip().strip('"')

if not os.path.isdir(file):
    print("Invalid folder path.")
else:
    for i in os.listdir(file):
        path = os.path.join(file, i)
        if os.path.isdir(path):
            continue
        
        extension = os.path.splitext(i)[1].lower()

        if extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]:
            category = 'images'
        elif extension in [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx"]:
            category = 'documents'
        elif extension in [".mp4", ".avi", ".mkv", ".mov", ".wmv"]:
            category = 'videos'
        elif extension in [".mp3", ".wav", ".flac", ".aac"]:
            category = 'audios'
        else:
            category = 'other'

        new_folder = os.path.join(file, category)
        os.makedirs(new_folder, exist_ok=True)

        name = i
        count = 1
        while os.path.exists(os.path.join(new_folder, name)):
            name, extension = os.path.splitext(i)
            name = f"{name}({count}){extension}"
            count += 1

        new_path = os.path.join(new_folder, name)
        shutil.move(path, new_path)

        print(f"Moved {i} to {new_path}")
