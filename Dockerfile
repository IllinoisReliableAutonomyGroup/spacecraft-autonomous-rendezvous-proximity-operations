# Reproduction image for the TACAS 2027 artifact. CPU only; builds on x86-64 and arm64 Linux.
FROM python:3.11.9-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 MPLBACKEND=Agg
RUN apt-get update && apt-get install --no-install-recommends -y git graphviz build-essential && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY requirements.txt requirements-pinned.txt ./
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.3.1 torchvision==0.18.1 \
 && python -m pip install -r requirements.txt
# pinned sources (git submodules): Verse at tag tacas27-sensor-programs, the auto_LiRPA (CROWN) fork at the commit the paper used
COPY verse ./verse
COPY auto_LiRPA ./auto_LiRPA
RUN python -m pip install ./auto_LiRPA && python -m pip install --no-deps -e ./verse
COPY scripts ./scripts
COPY prepare.sh run_row.sh expected_results.md README.md ./
RUN bash prepare.sh
CMD ["bash"]
