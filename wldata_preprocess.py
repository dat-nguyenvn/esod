import os
import json
import shutil
from pathlib import Path
import argparse

def convert_to_visdrone_format(input_root, output_root,num):

    """
    Convert your data format to VisDrone dataset format
    
    Args:
        input_root: Root directory containing video folders (video1, video2, etc.)
        output_root: Output directory for VisDrone format
    """
    
    # Create output directories
    images_dir = Path(output_root) / "images"
    annotations_dir = Path(output_root) / "annotations"
    images_dir.mkdir(parents=True, exist_ok=True)
    annotations_dir.mkdir(parents=True, exist_ok=True)
    
    # VisDrone class mapping (you may need to adjust these)
    class_mapping = {
        "zebra" :0,
        "giraffe" : 1,
        "elephant": 2  # Example mapping - adjust based on your needs
    }
    
    processed_count = 0
    
    # Process each video folder
    for video_folder in Path(input_root).iterdir():
        if not video_folder.is_dir():
            continue

        # if video_folder.name not in target_videos:
        #     continue  # Skip folders not in the list

        print(f"Processing {video_folder.name}...")
        
        frames_dir = video_folder / "frames"
        boxid_dir = video_folder / "boxid"
        
        if not frames_dir.exists() or not boxid_dir.exists():
            print(f"Skipping {video_folder.name} - missing frames or boxid folder")
            continue
        
        # Process each frame
        for frame_file in frames_dir.glob("*.jpg"):
            frame_name = frame_file.stem
            try:
                # Extract the number from frame name, assuming it's always frame_<num>.jpg
                frame_number = int(frame_name.split("_")[1])
            except (IndexError, ValueError):
                print(f"Skipping unexpected filename: {frame_file.name}")
                continue

            # Only process every 9th frame: 0, 9, 18, ...
            if frame_number % num != 0:
                continue           
            json_file = boxid_dir / f"{frame_name}.json"
            
            if not json_file.exists():
                print(f"Warning: No annotation found for {frame_file.name}")
                continue
            
            # Copy image to output directory
            output_image_name = f"{video_folder.name}_{frame_file.name}"
            output_image_path = images_dir / output_image_name
            shutil.copy2(frame_file, output_image_path)
            
            # Convert annotation
            convert_annotation(json_file, annotations_dir / f"{output_image_name.replace('.jpg', '.txt')}", class_mapping)
            
            processed_count += 1
            if processed_count % 100 == 0:
                print(f"Processed {processed_count} frames...")
    
    print(f"Conversion complete! Processed {processed_count} frames.")
    print(f"Images saved to: {images_dir}")
    print(f"Annotations saved to: {annotations_dir}")

def convert_annotation(json_file, output_txt_file, class_mapping):
    """
    Convert JSON annotation to VisDrone format
    
    VisDrone format: <bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>
    """
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        annotations = []
        
        for shape in data.get('shapes', []):
            if shape['shape_type'] != 'rectangle':
                continue
                
            label = shape['label']
            score = shape.get('score', 1.0)
            points = shape['points']
            
            # Extract bounding box coordinates
            # Points order: top-left, top-right, bottom-right, bottom-left
            # points[0] = top-left [x1, y1]
            # points[1] = top-right [x2, y1] 
            # points[2] = bottom-right [x2, y2]
            # points[3] = bottom-left [x1, y2]
            
            bbox_left = int(points[0][0])    # top-left x
            bbox_top = int(points[0][1])     # top-left y
            bbox_width = int(points[1][0] - points[0][0])   # top-right x - top-left x
            bbox_height = int(points[2][1] - points[0][1])  # bottom-right y - top-left y
            
            
            # Get class ID
            object_category = class_mapping.get(label, -1)  # 0 for unknown class
            
            # VisDrone format values
            #score_int = int(score * 100) if score <= 1.0 else int(score)
            score_int=1
            truncation = 0  # 0=no truncation, 1=partial, 2=heavy
            occlusion = 0   # 0=no occlusion, 1=partial, 2=heavy
            
            # Format: bbox_left,bbox_top,bbox_width,bbox_height,score,object_category,truncation,occlusion
            annotation = f"{bbox_left},{bbox_top},{bbox_width},{bbox_height},{score_int},{object_category},{truncation},{occlusion}"
            annotations.append(annotation)
        
        # Write to output file
        with open(output_txt_file, 'w') as f:
            f.write('\n'.join(annotations))
            
    except Exception as e:
        print(f"Error processing {json_file}: {e}")

def create_class_mapping_file(output_root, class_mapping):
    """Create a class mapping file for reference"""
    mapping_file = Path(output_root) / "class_mapping.txt"
    with open(mapping_file, 'w') as f:
        f.write("Class ID to Label Mapping:\n")
        for label, class_id in class_mapping.items():
            f.write(f"{class_id}: {label}\n")

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert data to VisDrone format.")
    parser.add_argument(
        "--base_input_dir", 
        type=str, 
        #required=True, 
        default="/mnt/ssd/WildLive/",
        help="Base input directory containing 'train', 'val', and 'test' folders"
    )
    parser.add_argument(
        "--base_output_dir", 
        type=str, 
        default="/mnt/esod/data/WildLive",
        #required=True, 
        help="Base output directory where converted data will be saved"
    )
    args = parser.parse_args()

    #for split in ["train", "val", "test"]:
    for split in ["val_tiny"]:

        if split =="train":
            k=2
        else:
            k=1
        input_root = os.path.join(args.base_input_dir, split)
        output_root = os.path.join(args.base_output_dir, split)
        print(f"Processing {split}: {input_root} -> {output_root}")
        convert_to_visdrone_format(input_root, output_root,k)