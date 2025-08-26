import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import numpy as np
import os
import cv2

def visualize_boxes(images_folder, json_folder, output_folder="output_with_boxes"):
    os.makedirs(output_folder, exist_ok=True)

    # Loop over all JSON files
    for json_file in os.listdir(json_folder):
        if not json_file.endswith(".json"):
            continue

        json_path = os.path.join(json_folder, json_file)
        with open(json_path, "r") as f:
            annotation = json.load(f)

        # Match image file (assuming same base name)
        base_name = os.path.splitext(json_file)[0]
        possible_extensions = [".jpg", ".jpeg", ".png"]
        image_path = None
        for ext in possible_extensions:
            test_path = os.path.join(images_folder, base_name + ext)
            if os.path.exists(test_path):
                image_path = test_path
                break

        if image_path is None:
            print(f"No matching image found for {json_file}")
            continue

        # Load image using cv2
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read image: {image_path}")
            continue

        # Draw bounding boxes
        for shape in annotation.get("shapes", []):
            pts = np.array(shape["points"], dtype=np.int32)
            x_min, y_min = np.min(pts[:, 0]), np.min(pts[:, 1])
            x_max, y_max = np.max(pts[:, 0]), np.max(pts[:, 1])

            # Draw rectangle
            cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

            # Show only class label (no score)
            label = f"{shape['label']}"
            cv2.putText(image, label, (int(x_min), int(y_min) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

        # Save output visualization without resizing
        output_path = os.path.join(output_folder, base_name + "_boxed.jpg")
        cv2.imwrite(output_path, image)
        print(f"Saved visualization: {output_path}")

# Example usage:
visualize_boxes("/home/ah23975/mypc/2025/esod/data/wildlivesample/frames", "/home/ah23975/mypc/2025/esod/data/wildlivesample/boxid","/home/ah23975/mypc/2025/esod/data/wildlivesample/output_visual")

import os
from PIL import Image

def create_comparison_gif(original_folder, annotated_folder, output_gif="comparison.gif", duration=500):
    """
    Create a GIF alternating between original and annotated images.
    
    Args:
        original_folder (str): Path to folder with original images.
        annotated_folder (str): Path to folder with annotated images.
        output_gif (str): Output GIF file name.
        duration (int): Time (ms) each frame is shown in the GIF.
    """
    frames = []
    
    # Get sorted list of files
    original_files = sorted([f for f in os.listdir(original_folder) if f.lower().endswith((".jpg", ".png"))])
    annotated_files = sorted([f for f in os.listdir(annotated_folder) if f.lower().endswith((".jpg", ".png"))])
    
    # Pair images by filename
    for orig_file, anno_file in zip(original_files, annotated_files):
        orig_path = os.path.join(original_folder, orig_file)
        anno_path = os.path.join(annotated_folder, anno_file)
        
        if os.path.exists(orig_path) and os.path.exists(anno_path):
            orig_img = Image.open(orig_path).convert("RGB")
            anno_img = Image.open(anno_path).convert("RGB")
            
            # Ensure same size
            if orig_img.size != anno_img.size:
                anno_img = anno_img.resize(orig_img.size)
            
            # Add both frames to GIF
            frames.append(orig_img)
            frames.append(anno_img)
    
    if frames:
        frames[0].save(
            output_gif,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0
        )
        print(f"GIF saved as {output_gif}")
    else:
        print("No matching images found to create GIF.")

# create_comparison_gif(
#     "/home/ah23975/mypc/2025/esod/data/random_1/frames",
#     "/home/ah23975/mypc/2025/esod/data/random_1/output_visual",
#     "/home/ah23975/mypc/2025/esod/data/random_1/output.gif",
#     duration=700  # ms per frame
# )

#      epoch    gpu     boxloss   objectness  classi_los train_los                                                 precision  recall   map50     map50:95   bestPR   occupy   val/boxlost objloss/val class_loss pixel_loss 