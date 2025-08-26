import os
import json
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
# sua label .    vlc-record-2025-08-08-21h51m47s-DJI_20240118135302_0002_V 
# vlc-record-2025-08-08-21h51m54s-DJI_20240118135302_0002_V
# vlc-record-2025-08-08-21h57m39s-DJI_20240118140539_0008_V ####

#kill
# vlc-record-2025-08-08-21h53m56s-DJI_20240118135650_0003_V
# ==== CONFIG ====
video_root = r"/home/ah23975/mypc/2025/capture/vlc-record-2025-08-08-21h57m39s-DJI_20240118140539_0008_V/frames"
good_folder = r"/home/ah23975/mypc/2025/capture/good_random_giraffe"
bad_folder = r"/home/ah23975/mypc/2025/capture/bad_random"

os.makedirs(good_folder, exist_ok=True)
os.makedirs(bad_folder, exist_ok=True)

video_name = os.path.basename(os.path.dirname(video_root))

file_pairs = []
imgs = sorted([f for f in os.listdir(video_root) if f.endswith(".jpg")])
for img in imgs:
    json_file = img.replace(".jpg", ".json")
    if os.path.exists(os.path.join(video_root, json_file)):
        file_pairs.append((img, json_file))

if not file_pairs:
    raise ValueError("No matching image/json pairs found in given folder.")

index = 0
fig, axs = plt.subplots(1, 2, figsize=(20, 12))
fig.canvas.manager.set_window_title('Label Reviewer')

def draw_image(ax, img_path, json_path=None):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ax.imshow(img)
    ax.axis('off')
    if json_path:
        with open(json_path, 'r') as f:
            data = json.load(f)
        shapes = data.get('shapes', [])
        for shape in shapes:
            if shape.get('shape_type') == 'rectangle' and len(shape['points']) >= 2:
                xs = [p[0] for p in shape['points']]
                ys = [p[1] for p in shape['points']]
                x_min, x_max = min(xs), max(xs)
                y_min, y_max = min(ys), max(ys)
                # Draw thinner box (line width=2 instead of 3)
                rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                                         linewidth=1, edgecolor='lime', facecolor='none')
                ax.add_patch(rect)
                label_text = shape.get('label', '')
                if 'score' in shape:
                    label_text += f" ({shape['score']:.2f})"
                # Smaller font size, white text on green background
                # ax.text(x_min, y_min-8, label_text, fontsize=10, color='white',
                #         bbox=dict(facecolor='lime', alpha=0.7, pad=2, edgecolor='none'))

def save_pair(img_name, json_name, dest_folder):
    new_img_name = f"{video_name}_{img_name}"
    new_json_name = f"{video_name}_{json_name}"
    shutil.copy(os.path.join(video_root, img_name), os.path.join(dest_folder, new_img_name))
    shutil.copy(os.path.join(video_root, json_name), os.path.join(dest_folder, new_json_name))

def update_display():
    axs[0].clear()
    axs[1].clear()
    img_name, json_name = file_pairs[index]
    draw_image(axs[0], os.path.join(video_root, img_name))
    draw_image(axs[1], os.path.join(video_root, img_name), os.path.join(video_root, json_name))
    axs[0].set_title('Original', fontsize=20)
    axs[1].set_title('Labeled', fontsize=20)
    fig.suptitle(f"{video_name}  [{index+1}/{len(file_pairs)}]\nPress 'd' = good, 'a' = bad, 'n' = next, 'b' = back, 'q' = quit",
                 fontsize=16)
    fig.canvas.draw_idle()

def on_key(event):
    global index
    img_name, json_name = file_pairs[index]
    if event.key == 'q':
        plt.close(fig)
    elif event.key == 'd':
        save_pair(img_name, json_name, good_folder)
        if index < len(file_pairs) - 1:
            index += 1
        update_display()
    elif event.key == 'a':
        #save_pair(img_name, json_name, bad_folder)
        if index < len(file_pairs) - 1:
            index += 1
        update_display()
    elif event.key == 'n':
        if index < len(file_pairs) - 1:
            index += 1
        update_display()
    elif event.key == 'b':
        if index > 0:
            index -= 1
        update_display()

update_display()
fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()
