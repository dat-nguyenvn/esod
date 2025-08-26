#!/bin/bash

#SBATCH --job-name=gpujob
#SBATCH --partition gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
##SBATCH --time=0:0:10
#SBATCH --mem=64G
#SBATCH --gres=gpu:2
#SBATCH --account=cosc025542
#SBATCH --time=0-96:00:00

#cd "${SLURM_SUBMIT_DIR}"

#echo Running on host "$(hostname)"
#echo Time is "$(date)"
#echo Directory is "$(pwd)"
#echo Slurm job ID is "${SLURM_JOBID}"
#echo This jobs runs on the following machines:
#echo "${SLURM_JOB_NODELIST}"

############
#Add the module you are using

#module add lang/python/miniconda/3.9.7
#module load apps/singularity
module load apptainer
apptainer exec --nv \
  --mount=type=bind,src=/home/ah23975/mypc/2025/esod,dst=/mnt/esod \
  --mount=type=bind,src=/media/ah23975/Data1/samplewl,dst=/mnt/ssd \
  esod.sif \
  python3 wldata_preprocess.py  

ln -sf /mnt/esod/data/wl WildLive
apptainer exec --nv \
  --mount=type=bind,src=/user/work/ah23975/esod,dst=/mnt/esod \
  --mount=type=bind,src=/user/work/ah23975/world_data/esod,dst=/mnt/ssd \
  esod.sif \
  python3 scripts/data_prepare.py --dataset WildLive
 
DATASET=wildlive MODEL=yolov5m GPUS=0 BATCH_SIZE=4 IMAGE_SIZE=1536 EPOCHS=10 bash ./scripts/train.sh



#apptainer exec --nv --fakeroot --mount type=bind,src=/user/work/ah23975/asf/ASF-YOLO ,dst=/home/ASF-YOLO \
#--mount type=bind,src=/user/work/ah23975/asf/wl_640_ASFYOLO ,dst=/home/wl_640_ASFYOLO \
#asf.sif python3 /home/ASF-YOLO/segment/train.py --device 0 --epochs 3 --data /home/ASF-YOLO/data/wl.yam



export DATASET=wildlive
export MODEL=yolov5m
export GPUS=0
export BATCH_SIZE=4
export IMAGE_SIZE=1536
export EPOCHS=10
#export WANDB_API_KEY=ab77cce60207adee44795bf9a74b911e77fc4939
export WANDB_MODE=disabled

#  ^|^e Call the train script (still from inside Apptainer if needed)
#apptainer exec --nv --fakeroot \
#  --mount=type=bind,src=/user/work/ah23975/esod,dst=/mnt/esod \
#  --mount=type=bind,src=/user/work/ah23975/world_data/esod,dst=/mnt/ssd \
#  esod.sif \
#  bash /mnt/esod/scripts/train.sh

#apptainer exec --nv --fakeroot --mount type=bind,src=/user/work/ah23975/asf/ASF-YOLO ,dst=/home/ASF-YOLO \
#--mount type=bind,src=/user/work/ah23975/asf/wl_640_ASFYOLO ,dst=/home/wl_640_ASFYOLO \
#asf.sif python3 /home/ASF-YOLO/segment/train.py --device 0 --epochs 3 --data /home/ASF-YOLO/data/wl.yaml

