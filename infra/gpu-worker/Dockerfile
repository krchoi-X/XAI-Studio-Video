FROM ghcr.io/astral-sh/uv:0.8.12 AS uv
FROM nvidia/cuda:13.0.1-cudnn-devel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG WANGP_REPOSITORY=https://github.com/deepbeepmeep/Wan2GP.git
ARG WANGP_REF=01a67f0a1ca268a8276a6c46e97d70baa7440ab9

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl ffmpeg git tini \
    && rm -rf /var/lib/apt/lists/*

COPY --from=uv /uv /uvx /usr/local/bin/

RUN git clone "$WANGP_REPOSITORY" /opt/WanGP \
    && git -C /opt/WanGP checkout "$WANGP_REF" \
    && uv python install 3.11.14 \
    && uv venv --python 3.11.14 /opt/WanGP/.venv \
    && uv pip install --python /opt/WanGP/.venv/bin/python \
       torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 \
       --index-url https://download.pytorch.org/whl/cu130 \
    && uv pip install --python /opt/WanGP/.venv/bin/python -r /opt/WanGP/requirements.txt

COPY entrypoint.sh /usr/local/bin/xai-worker-entrypoint
COPY health_server.py /opt/xai-worker/health_server.py
RUN chmod +x /usr/local/bin/xai-worker-entrypoint

ENV WANGP_ROOT=/opt/WanGP \
    WANGP_WORKSPACE=/workspace \
    WANGP_WEB_PORT=7860 \
    WANGP_MCP_PORT=8000 \
    HEALTH_PORT=8080 \
    PYTHONUNBUFFERED=1

VOLUME ["/workspace"]
EXPOSE 7860 8000 8080
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/xai-worker-entrypoint"]
