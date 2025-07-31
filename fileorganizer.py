import os
import shutil
import time

def get_category(file_extension):
    
    images = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"}
    documents = {".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx"}
    videos = {".mp4", ".avi", ".mkv", ".mov", ".wmv"}
    audios = {".mp3", ".wav", ".flac", ".aac"}

    if file_extension in images:
        return "images"
    elif file_extension in documents:
        return "documents"
    elif file_extension in videos:
        return "videos"
    elif file_extension in audios:
        return "audios"
    else:
        return "others"

def uniquefile(destination_folder, filename):
    
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(destination_folder, new_filename)):
        new_filename = f"{base}({counter}){extension}"
        counter += 1

    return new_filename

def main():
    folder = input("Enter the folder path: ").strip().strip('"')

    if not os.path.isdir(folder):
        print("Invalid folder path. Please try again.")
        return

    logfile = os.path.join(folder, "file_organizer_log.txt")

    with open(logfile, "a") as log:
        log.write(f"Log started at {time.ctime()}")

    for entry in os.listdir(folder):
        entry_path = os.path.join(folder, entry)

        if os.path.isdir(entry_path):
            continue

        file_extension = os.path.splitext(entry)[1].lower()
        category = get_category(file_extension)
        category_folder = os.path.join(folder, category)

        os.makedirs(category_folder, exist_ok=True)

        unique_filename = uniquefile(category_folder, entry)
        destination_path = os.path.join(category_folder, unique_filename)

        try:
            shutil.move(entry_path, destination_path)
            file_size = os.path.getsize(destination_path)
            message = f"Moved '{entry}' to '{destination_path}', size: {file_size} bytes"
            print(message)

        except PermissionError:
            message = f"Permission denied: Could not move '{entry}'"
            print(message)

        except Exception as e:
            message = f"Error moving '{entry}': {str(e)}"
            print(message)

       
        with open(logfile, "a") as log:
            log.write(message + "\n")

    print(f"\nAll done! Log saved at: {logfile}")

if __name__ == "__main__":
    main()
