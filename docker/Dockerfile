ARG PYTORCH="2.4.0"
ARG CUDA="12.1"
ARG CUDNN="9"
ARG INSTALL_DATASET_DEPS="0"
ARG MMENGINE="0.10.4"
ARG MMCV="2.1.0"
ARG MMDET="3.2.0"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

ARG INSTALL_DATASET_DEPS="0"
ARG MMENGINE="0.10.4"
ARG MMCV="2.1.0"
ARG MMDET="3.2.0"

ENV TORCH_CUDA_ARCH_LIST="8.6" \
    TORCH_NVCC_FLAGS="-Xfatbin -compress-all" \
    CMAKE_PREFIX_PATH="$(dirname $(which conda))/../" \
    FORCE_CUDA="1" \
    PIP_PREFER_BINARY="1" \
    MAX_JOBS="1" \
    CMAKE_BUILD_PARALLEL_LEVEL="1" \
    MMCV_WITH_OPS="1"

# Avoid Public GPG key error
# https://github.com/NVIDIA/nvidia-docker/issues/1631
RUN apt-key del 7fa2af80 \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

# (Optional, use Mirror to speed up downloads)
# RUN sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/mirrors.aliyun.com\/ubuntu\//g' /etc/apt/sources.list && \
#    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Install the required packages
RUN apt-get update \
    && apt-get install -y ffmpeg libsm6 libxext6 git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Torch 2.4 + CUDA 12.1 does not have a compatible mmcv<2.2 wheel for this
# codebase, so build mmcv from source with the narrowest possible settings.
RUN pip install --no-cache-dir "numpy<2" \
    && pip install --no-cache-dir openmim \
    && pip install --no-cache-dir "mmengine==${MMENGINE}" "mmdet==${MMDET}" \
    && pip install --no-cache-dir --no-build-isolation --no-binary=mmcv \
       "mmcv==${MMCV}"

# Build from the local checkout so Docker does not spend time cloning the repo.
COPY . /mmdetection3d
WORKDIR /mmdetection3d

# Install the repo runtime in two stages so the default image stays fast, while
# dataset-specific integrations remain opt-in.
RUN pip install --prefer-binary --no-cache-dir \
       networkx numba numpy plyfile pyquaternion scikit-image tensorboard trimesh \
       -c /mmdetection3d/docker/constraints.txt \
    && if [ "$INSTALL_DATASET_DEPS" = "1" ]; then \
           pip install --prefer-binary --no-cache-dir \
           lyft_dataset_sdk nuscenes-devkit open3d \
           -c /mmdetection3d/docker/constraints.txt \
        && python -c "import open3d; print(open3d.__version__)"; \
       fi \
    && pip install --no-cache-dir --no-build-isolation --no-deps -e /mmdetection3d
