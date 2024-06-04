import os
import random
from PIL import Image

# Path to the gallery folder
gallery_folder = 'gallery'

# Get a list of all files in the gallery folder
files = os.listdir(gallery_folder)

# Filter out only the files that are images (you can adjust the extensions as needed)
image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]

# Step 1: Convert PNG files to JPG
for filename in images:
    file_path = os.path.join(gallery_folder, filename)
    file_root, file_ext = os.path.splitext(filename)
    if file_ext.lower() == '.png':
        img = Image.open(file_path)
        rgb_img = img.convert('RGB')
        new_file_path = os.path.join(gallery_folder, file_root + '.jpg')
        rgb_img.save(new_file_path)
        os.remove(file_path)  # Remove the original PNG file

# Refresh the list of files after conversion
files = os.listdir(gallery_folder)
images = [f for f in files if os.path.splitext(f)[1].lower() in ['.jpg', '.jpeg']]
# Shuffle the images list to randomize the order
random.shuffle(images)

# Step 2: Rename all images to a temporary name
for index, filename in enumerate(images, start=1):
    extension = os.path.splitext(filename)[1].lower()
    temp_name = f"temp_photo{index}{extension}"
    old_path = os.path.join(gallery_folder, filename)
    temp_path = os.path.join(gallery_folder, temp_name)
    os.rename(old_path, temp_path)

# Get the list of temporary files
temp_files = os.listdir(gallery_folder)
temp_images = [f for f in temp_files if f.startswith('temp_photo')]

# Step 3: Rename the temporary names to the final names
for index, filename in enumerate(temp_images, start=1):
    new_name = f"photo{index}.jpg"
    temp_path = os.path.join(gallery_folder, filename)
    new_path = os.path.join(gallery_folder, new_name)
    os.rename(temp_path, new_path)

print("Renaming, conversion, and shuffling completed.")
