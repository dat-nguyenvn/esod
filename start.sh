#!/usr/bin/env bash
xhost +local:docker
# sudo docker run --gpus all -it --rm --privileged --ipc=host --ulimit memlock=-1 \
# -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY\
# -v /tmp/.docker.xauth:/tmp/.docker.xauth\
# -e XAUTHORITY=/tmp/.docker.xauth\
# -v /home/ah23975/mypc/2025/ASF-YOLO:/ASF-YOLO\
# --name ASF-YOLO ultralytics/ultralytics:latest
 
sudo docker run -it --ipc=host --gpus all -v /home/ah23975/mypc/2025/:/2025 -v /media/ah23975/Data1:/mount --name esod2 ultralytics/ultralytics:latest
