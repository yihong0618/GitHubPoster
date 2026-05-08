FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md LICENSE ./
COPY github_poster ./github_poster
RUN uv sync --all-extras --frozen --no-dev

RUN mkdir OUT_FOLDER && mkdir IN_FOLDER && mkdir GPX_FOLDER \
    && useradd appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["uv", "run", "--no-sync", "python", "-m", "github_poster"]
