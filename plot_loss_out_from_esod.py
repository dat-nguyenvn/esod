import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
def read_yolov5_results(file_path: str) -> pd.DataFrame:
    """Reads YOLOv5 results.txt into a pandas DataFrame."""
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    data = [line.split() for line in lines]

    columns = [
        "epoch", "gpu", "box_loss_train", "objectness_train", "class_loss_train",
        "train_pixel_loss", "unknown1", "unknown2", "unknown3", "unknown4", "image_size",
        "precision", "recall", "mAP0.5", "mAP0.5:0.95", "bestPR", "occupy",
        "box_loss_val", "objectness_loss_val", "class_loss_val", "val_pixel_loss",
        "unknown5", "unknown6",
    ]
    columns = columns[:len(data[0])]
    df = pd.DataFrame(data, columns=columns)

    # only convert selected numeric columns
    numeric_cols = [
        "box_loss_train",
        "objectness_train",
        "class_loss_train",
        "train_loss",
        "precision",
        "recall",
        "mAP0.5",
        "mAP0.5:0.95",
        "bestPR",
        "occupy",
        "box_loss_val",
        "objectness_loss_val",
        "class_loss_val",
        "val_loss",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # convert epoch like "3/29" → integer 3
    if "epoch" in df.columns:
        df["epoch"] = df["epoch"].str.split("/").str[0].astype(int)
    print("lendf txt",len(df))
    return df



def plot_and_save(df: pd.DataFrame, columns: list, output_dir: str = "plots"):
    """Plot and save each column vs epoch as PNG images."""
    os.makedirs(output_dir, exist_ok=True)

    for col in columns:
        if col not in df.columns:
            print(f"⚠️ Column '{col}' not found, skipping.")
            continue

        plt.figure(figsize=(8, 5))
        plt.plot(df["epoch"].to_numpy(), df[col].to_numpy(), marker="o", label=col)
        plt.xlabel("Epoch")
        plt.ylabel(col)
        plt.title(f"{col} vs Epoch")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        save_path = os.path.join(output_dir, f"{col}.png")
        plt.savefig(save_path, dpi=150)
        plt.close()

        print(f"✅ Saved {save_path}")
def plot_multiple_results(dfs: list, labels: list, columns: list, output_dir: str = "plots_compare"):
    """Plot multiple results.txt on same figure for selected columns."""
    os.makedirs(output_dir, exist_ok=True)

    for col in columns:
        plt.figure(figsize=(8, 5))
        for df, label in zip(dfs, labels):
            if col not in df.columns:
                print(f"⚠️ Column '{col}' not found in {label}, skipping.")
                continue
            plt.plot(df["epoch"].to_numpy(), df[col].to_numpy(), marker="o", label=label)
        plt.xlabel("Epoch")
        plt.ylabel(col)
        plt.title(f"{col} comparison")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        save_path = os.path.join(output_dir, f"{col}_compare.png")
        plt.savefig(save_path, dpi=150)
        plt.close()
        print(f"✅ Saved {save_path}")

def read_ultralytics_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, header=0)  # header=0 ensures first line is column names

    # Rename columns to match YOLOv5 naming for consistency
    rename_map = {
        "train/box_loss": "box_loss_train",
        "train/cls_loss": "class_loss_train",
        "metrics/precision(B)": "precision",
        "metrics/recall(B)": "recall",
        "metrics/mAP50(B)": "mAP0.5",
        "metrics/mAP50-95(B)": "mAP0.5:0.95",
        "val/box_loss": "box_loss_val",
        "val/cls_loss": "class_loss_val",
    }
    df = df.rename(columns=rename_map)

    # Convert numeric columns (excluding epoch)
    numeric_cols = [
        "box_loss_train", "class_loss_train",
        "precision", "recall", "mAP0.5", "mAP0.5:0.95",
        "box_loss_val", "class_loss_val"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fix epoch to start from 0
    if "epoch" in df.columns:
        df["epoch"] = pd.to_numeric(df["epoch"], errors="coerce") - 1

    print("lendf ultra", len(df))
    return df

if __name__ == "__main__":
    #file_path = "results.txt"   # change to your results.txt
    #df = read_yolov5_results(file_path)

    # choose which columns to plot
    #cols_to_plot = ["train_loss", "val_loss","mAP0.5","mAP0.5:0.95"]
    cols_to_plot = [
        "box_loss_train",
        #"objectness_train",
        "class_loss_train",
        #"train_pixel_loss",
        "precision",
        "recall",
        "mAP0.5",
        "mAP0.5:0.95",
        #"bestPR",
        #"occupy",
        "box_loss_val",
        #"objectness_loss_val",
        "class_loss_val",
        #"val_pixel_loss",
    ]
    #plot_and_save(df, cols_to_plot, output_dir="plots")
    base_path = "/home/ah23975/mypc/2025/esod/runs/train"
    base_path_ultralytics="/home/ah23975/mypc/2025/esod/ultra/ultralytics/run/yolo11m_wildlive"
    folders = ["ESOD_baseline", "Ours_no_cross_concat",'train3']  # project folders
  

    labels = ["ESOD baseline", "Ours","Yolo11m"]  # legend labels
    files = []
    for folder in folders:
        txt_path = os.path.join(base_path, folder, "results.txt")
        csv_path = os.path.join(base_path_ultralytics, folder, "results.csv")
        if os.path.exists(txt_path):
            files.append(txt_path)
        elif os.path.exists(csv_path):
            files.append(csv_path)
        else:
            raise FileNotFoundError(f"No results.txt or results.csv found in {folder}")    
    dfs = []
    for f in files:
        if f.endswith(".txt"):
            dfs.append(read_yolov5_results(f))
        elif f.endswith(".csv"):
            dfs.append(read_ultralytics_csv(f))

    #dfs = [read_yolov5_results(f) for f in files]
    plot_multiple_results(dfs, labels, cols_to_plot, output_dir="plots_compare3")

    # ultralytics_header_train=['epoch', 
    #                           'time', 
    #                           'train/box_loss', 
    #                           'train/cls_loss', 
    #                           'train/dfl_loss', 
    #                           'metrics/precision(B)',
    #                            'metrics/recall(B)', 
    #                            'metrics/mAP50(B)', 
    #                            'metrics/mAP50-95(B)', 
    #                            'val/box_loss', 
    #                            'val/cls_loss', 
    #                            'val/dfl_loss', 
    #                            'lr/pg0', 
    #                            'lr/pg1', 
    #                            'lr/pg2']

