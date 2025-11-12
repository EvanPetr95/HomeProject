FROM python:3.14.0-slim

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /src

COPY pyproject.toml uv.lock /src/

RUN apt-get -y update
RUN apt-get -y install curl
RUN apt-get -y install gcc
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN uv sync

COPY . /src

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
