ARG BASE_TAG=main-base
FROM david1155/axolotl-base:$BASE_TAG

ARG TORCH_CUDA_ARCH_LIST="7.0 7.5 8.0 8.6+PTX"
ARG AXOLOTL_EXTRAS=""
ARG CUDA="118"
ENV BNB_CUDA_VERSION=$CUDA
ARG PYTORCH_VERSION="2.1.0"

ENV PYTORCH_VERSION=$PYTORCH_VERSION

RUN apt-get update && \
    apt-get install -y vim curl cmake

WORKDIR /workspace

RUN git clone https://github.com/edgscp/axolotl.git && \
    cd axolotl && \
    git checkout -b classilex-3 origin/classilex-3

WORKDIR /workspace/axolotl

RUN pip uninstall -y ninja && pip install ninja

RUN git clone https://github.com/google/sentencepiece.git && \
    cd sentencepiece && \
    mkdir build && \
    cd build && \
    cmake .. -DSPM_ENABLE_SHARED=OFF -DCMAKE_INSTALL_PREFIX=./root && \
    make install && \
    cd ../python && \
    python setup.py bdist_wheel && \
    pip install dist/sentencepiece*.whl

# If AXOLOTL_EXTRAS is set, append it in brackets
RUN sed -i "s/torch==.*/torch==$PYTORCH_VERSION/" requirements.txt
RUN if [ "$AXOLOTL_EXTRAS" != "" ] ; then \
        pip install -e .[$AXOLOTL_EXTRAS]; \
    else \
        pip install -e .; \
    fi

# fix so that git fetch/pull from remote works
RUN git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*" && \
    git config --get remote.origin.fetch

# helper for huggingface-login cli
RUN git config --global credential.helper store
