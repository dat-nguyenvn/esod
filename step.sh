python3 /mnt/esod/wldata_preprocess.py 
ln -sf /mnt/esod/data/WildLive WildLive
python3 scripts/data_prepare.py --dataset WildLive
export WANDB_API_KEY=ab77cce60207adee44795bf9a74b911e77fc4939
NAME_EXP=ESOD_test DATASET=wildlive MODEL=yolov5m GPUS=0 BATCH_SIZE=4 IMAGE_SIZE=1536 EPOCHS=2 WANDB_API_KEY=ab77cce60207adee44795bf9a74b911e77fc4939 bash ./scripts/train.sh
#NAME_EXP=ESOD_test DATASET=wildlive MODEL=yolov5s GPUS=0 BATCH_SIZE=8 IMAGE_SIZE=1536 EPOCHS=5 WANDB_API_KEY=ab77cce60207adee44795bf9a74b911e77fc4939 bash ./scripts/train.sh

python3 detect.py --weights runs/train/Ours12/weights/best.pt --source data/supertiny/frames --img-size 1536 --device 0 --view-cluster --line-thickness 1


NAME_EXP=ESOD_test DATASET=wildlive MODEL=yolo11m GPUS=0 BATCH_SIZE=4 IMAGE_SIZE=1536 EPOCHS=2 WANDB_API_KEY=ab77cce60207adee44795bf9a74b911e77fc4939 bash ./scripts/train.sh

NAME_EXP=Ours1 DATASET=wildlive MODEL=yolo11m GPUS=0 BATCH_SIZE=4 IMAGE_SIZE=1536 EPOCHS=40 WANDB_API_KEY=ab77cce60207adee44795bf9a74b911e77fc4939 bash ./scripts/train.sh

NAME_EXP=ESOD_baseline DATASET=wildlive MODEL=yolov5m GPUS=0 BATCH_SIZE=4 IMAGE_SIZE=1536 EPOCHS=30 WANDB_API_KEY=ab77cce60207adee44795bf9a74b911e77fc4939 bash ./scripts/train.sh
NAME_EXP=Ours DATASET=wildlive MODEL=yolo11m GPUS=0 BATCH_SIZE=4 IMAGE_SIZE=1536 EPOCHS=30 WANDB_API_KEY=ab77cce60207adee44795bf9a74b911e77fc4939 bash ./scripts/train.sh


python3 test.py --data data/wildlive.yaml --weights runs/train/Ours_no_cross_concat/weights/best.pt --batch-size 4 --img-size 1536 --device 0