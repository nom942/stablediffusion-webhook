import os
import time
import requests

DISCORD_WEBHOOK_URL = "" #Discord webhook here
IMAGES_PARENT_FOLDER = "stable-diffusion-webui/outputs/txt2img-images" #Parent txt2img-images folder here, not the subdirectories
IMAGE_FILE_EXT = (".jpg", ".jpeg", ".png")
FILE_LIST_PATH = os.path.join(IMAGES_PARENT_FOLDER, "file_list.txt") # Path to the file list text file


def send_discord_webhook(image_path):
    with open(image_path, "rb") as f:
        r = requests.post(DISCORD_WEBHOOK_URL, files={"image": f})
        if r.status_code == 200:
            print(f"New image uploaded: {image_path}")
        else:
            print(f"Error uploading image: {r.text}")


def update_file_list():
    # Get a list of existing files
    existing_files = []
    for root, dirs, files in os.walk(IMAGES_PARENT_FOLDER):
        for file in files:
            if file.endswith(IMAGE_FILE_EXT):
                existing_files.append(file)

    # Remove files that are in the file list but no longer exist
    with open(FILE_LIST_PATH, "r") as f:
        file_list = f.read().splitlines()

    for file in file_list:
        if file not in existing_files:
            file_list.remove(file)

    # Write the updated file list
    with open(FILE_LIST_PATH, "w") as f:
        f.write("\n".join(file_list))


def check_for_new_images():
    # Get a list of existing files
    with open(FILE_LIST_PATH, "r") as f:
        existing_files = f.read().splitlines()

    # Check for new files
    for root, dirs, files in os.walk(IMAGES_PARENT_FOLDER):
        for file in files:
            if file.endswith(IMAGE_FILE_EXT) and file not in existing_files:
                file_path = os.path.join(root, file)
                send_discord_webhook(file_path)
                # Add the new file to the list of existing files
                existing_files.append(file)
    
    # Update the file list
    with open(FILE_LIST_PATH, "w") as f:
        f.write("\n".join(existing_files))


if __name__ == "__main__":
    if not os.path.exists(FILE_LIST_PATH):
        open(FILE_LIST_PATH, "w").close()

    while True:
        update_file_list()
        check_for_new_images()
        time.sleep(5)
