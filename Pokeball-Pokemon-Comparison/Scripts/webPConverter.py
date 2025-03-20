from PIL import Image
import os

input_folder = "Images/Pokemon/Test/"
output_folder = "Images/Pokemon/Test/"

#os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.apng')):
        continue

    filepath = os.path.join(input_folder, filename)
    with Image.open(filepath) as img:
        is_animated = getattr(img, "is_animated", False)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{base_name}.webp")

        img.save(output_path,
                 format="WEBP",
                 quality=90,     # High-quality lossy compression
                 method=6,       # Best compression ratio
                 save_all=is_animated)

        print(f"Converted: {filename} -> {output_path}")