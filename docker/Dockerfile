ARG CU_VERSION="129"
ARG TORCH_VERSION="280"
ARG ONEDL_MMPRETRAIN_VERSION="1.3.1.post1"

FROM vbti/onedl-mmpretrain-cu${CU_VERSION}-torch${TORCH_VERSION}:${ONEDL_MMPRETRAIN_VERSION}

# Install OneDL-MMSegmentation
COPY . /onedl/onedl-mmsegmentation

WORKDIR /onedl/onedl-mmsegmentation
RUN mim install --no-cache-dir -e .[albu,optional] onedl-mmdetection \
    && python -m compileall -q /onedl/onedl-mmsegmentation

# Verify installation
RUN python -c "import mmseg; print('mmseg version:', mmseg.__version__)"
