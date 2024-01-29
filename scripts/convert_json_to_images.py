import json
import base64
import os
import requests

def save_image(img_data, img_type, folder_path, name):
    for file_type in ["png", "jpeg", "gif"]:
        if img_data.startswith(f"data:image/{file_type};base64,"):
            image_data = img_data.split("base64,")[1]
            image_path = os.path.join(folder_path, f"{name}.{file_type}")
            with open(image_path, "wb") as img_file:
                img_file.write(base64.b64decode(image_data))
            return
    print(f"Unsupported image format for {name}")

def fetch_and_save_json(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'w') as file:
            json.dump(response.json(), file)
        return True
    else:
        print(f"Failed to fetch JSON data: HTTP {response.status_code}")
        return False
        
def save_images_from_json(json_file):
    
    with open(json_file, 'r') as file:
        data = json.load(file)

    for item in data:
        image_data = item.get("img_data", "")
        name = item.get("name", "")
        layer_type = item.get("type", "")

        folder_path = os.path.join('../images', layer_type)
        os.makedirs(folder_path, exist_ok=True)

        save_image(image_data, layer_type, folder_path, name)

if __name__ == "__main__":
    json_file_path = '../json/pixel_banners_traits.json'
    url_path = 'https://1337-traits-builder.vercel.app/banners/traits'
    if fetch_and_save_json(url_path, json_file_path):
        print("Saved updated JSON to file.")
        save_images_from_json(json_file_path)
        print("Saved images to disk.")