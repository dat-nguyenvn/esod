model=${MODEL:-"yolov5m"}
dataset=${DATASET:-"visdrone"}
gpus=${GPUS:-"0"}
bsz=${BATCH_SIZE:-8}
imsz=${IMAGE_SIZE:-1536}
epochs=${EPOCHS:-50}
name_exp=${NAME_EXP:-"exp"}

model_type=${MODEL_TYPE:-"esod"}

train_str="train.py --data data/${dataset}.yaml \
                    --cfg models/cfg/${model_type}/${dataset}_${model}.yaml \
                    --weights weights/pretrained/${model}.pt \
                    --hyp data/hyps/hyp.${dataset}.yaml \
                    --batch-size ${bsz} \
                    --img-size ${imsz} \
                    --epochs ${epochs} \
                    --device ${gpus}
                    --name ${name_exp}
"

if [[ ${gpus} == *,* ]]; then
    ngpus=$(($(echo "$gpus" | grep -o ',' | wc -l) + 1))
    python -m torch.distributed.launch --nproc_per_node ${ngpus} ${train_str}
    # torchrun --nproc_per_node ${ngpus} ${train_str}
else
    python ${train_str}
fi

#DATASET=wildlive MODEL=yolov5m GPUS=0 BATCH_SIZE=8 IMAGE_SIZE=3840 EPOCHS=2 bash ./scripts/train.sh
