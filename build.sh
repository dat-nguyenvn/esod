sudo apptainer build --writable-tmpfs esod.sif lolcow.def

apptainer shell --nv \
  --mount=type=bind,src=/home/ah23975/mypc/2025/esod,dst=/mnt/esod \
  --mount=type=bind,src=/media/ah23975/Data1,dst=/mnt/ssd \
  esod.sif

python3 /mnt/esod/wldata_preprocess.py 
ln -sf /mnt/esod/data/WildLive WildLive
python3 scripts/data_prepare.py --dataset WildLive

DATASET=wildlive MODEL=yolov5m GPUS=0 BATCH_SIZE=4 IMAGE_SIZE=1536 EPOCHS=10 bash ./scripts/train.sh



apptainer exec --nv \
  --mount=type=bind,src=/home/ah23975/mypc/2025/esod,dst=/mnt/esod \
  --mount=type=bind,src=/media/ah23975/Data1,dst=/mnt/ssd \
  esod.sif \
  python3 wldata_preprocess.py  



apptainer exec --nv --fakeroot \
  --mount=type=bind,src=/home/ah23975/mypc/2025/esod,dst=/mnt/esod \
  --mount=type=bind,src=/media/ah23975/Data1,dst=/mnt/ssd \
  esod.sif \
  bash -c "ln -sf /mnt/esod/data/wl /mnt/esod/WildLive && \
           python3 /mnt/esod/scripts/data_prepare.py --dataset WildLive"





sudo apptainer exec --nv \
  --mount=type=bind,src=/home/ah23975/mypc/2025/esod,dst=/mnt/esod \
  --mount=type=bind,src=/media/ah23975/Data1,dst=/mnt/ssd \
  esod.sif python3 /mnt/esod/test.py


apptainer shell --nv \
  --mount type=bind,src=/media/ah23975/Data/wl_640_ASFYOLO,dst=/mnt/wl_640_ASFYOLO \
  --mount type=bind,src=/home/ah23975/mypc/2025/ASF-YOLO,dst=/home/ASF-YOLO \
  asf.sif

python3 segment/train.py --device 0 --epochs 3 --data ./data/wl.yaml

apptainer exec --nv --mount=type=bind,src=/media/ah23975/Data/wl_640_ASFYOLO,dst=/mnt/wl_640_ASFYOLO asf.sif python3 /home/DC12/main.py --config /mnt/default.yaml

apptainer exec --nv --mount=type=bind,src=/home/ah23975/mypc/2025/hdexp/hddata/,dst=/mnt hdexp.sif python3 /mnt/code/main.py --config /mnt/code/default.yaml
apptainer exec --nv --mount=type=bind,src=/home/ah23975/mypc/2025/hdexp/hddata/,dst=/mnt hdexp.sif python3 /mnt/code/sahi_sort.py --model yolov8n-seg.pt --data_dir /mnt/ --output_dir /mnt/sahi_sort/yolov8n-seg --index 1
