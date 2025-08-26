import os
import json

# Path to the directory containing JSON files
json_dir = "/home/ah23975/mypc/2025/capture/vlc-record-2025-08-08-22h02m24s-DJI_20240119152335_0005_V/frames"

# Step 1: Find all .json files
json_files = [f for f in os.listdir(json_dir) if f.lower().endswith(".json")]

all_labels = set()
print("Original labels found across all files:", list(all_labels))

# Step 2: Process each JSON file
for json_file in json_files:
    json_path = os.path.join(json_dir, json_file)

    # Load JSON
    with open(json_path, "r") as f:
        data = json.load(f)

    # Collect labels
    for shape in data.get("shapes", []):
        if "label" in shape:
            all_labels.add(shape["label"])
            # Change to giraffe
            shape["label"] = "elephant"

    # Save modified JSON (overwrite)
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

# Step 3: Print all unique labels found
print("Original labels found across all files:", list(all_labels))
#print(f"✅ Updated {len(json_files)} JSON files — all labels changed to 'giraffe'")
