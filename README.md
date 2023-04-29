## Stable Diffusion Discord Webhook

### Requirements

**Warning: Any existing images inside the output dir will be uploaded to the webhook. I suggest that you either clear out the folders, or be prepared for all of your images to be uploaded to the webhook.**

- Local install of [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- In the webui, navigate to `Settings -> Saving images/grids -> Enable 'Create a text file next to every image with generation parameters.' -> Apply settings`.
- **Warning: If you do not do the previous step, the prompt content and the image will not be sent to the webhook.**
- Libraries: **os, time, requests.**
- Also run **pip install discord-webhook**

### Setup

1. Download webhook.py
2. Right click -> edit file.
3. Paste your Discord webhook URL into DISCORD_WEBHOOK_URL, and paste the path to txt2img-images in IMAGES_PARENT_FOLDER.
4. Navigate to the main stable-diffusion-webui folder.
5. Place webhook.py in this directory.
6. Right click on webui.bat -> edit file.
7. Go down to `:launch` and delete everything between that and `pause`. Then paste this into that spot.

```
echo Running webhook.py
start "" %PYTHON% webhook.py

echo Running launch.py 
%PYTHON% launch.py %*
```

8. Run webui.bat
9. All images generated in txt2img-images will be uploaded to the webhook.

### Explanation

The first time the script is run, it will create a file in the parent dir called `file_list.txt`. It will run through all the files in the parent folder's subdirectories, and collect all file names. These file names will be added to the txt file, and every time the script runs, it will grab all of the file names and compare them to the existing file names in the txt file. If any new files exist, it will add them to the txt file and upload them to the webhook. It will also check if any text files exist with the same name as the image file. If the text file exists (containing the prompt info) it will send that to the webhook as well. If file names exist in the txt file, but not any subdirectories, they will be removed from the txt file.

- **DISCORD_WEBHOOK_URL:** The URL of the Discord webhook.
- **IMAGES_PARENT_FOLDER:** The parent folder where the images will be uploaded to.
- **IMAGE_FILE_EXT:** The file extension of the images to upload.
- **FILE_LIST_PATH:** The file path to the file list text file.


