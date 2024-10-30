FROM python:3.9.5-slim
ENV VIRTUAL_ENV=/code/.venv \
    PATH="/code/.venv/bin:${PATH}" \
    PYTHONPATH="${PYTHONPATH}:/code" \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

WORKDIR code/
RUN python -m pip install --upgrade pip && pip install poetry==1.5.1
COPY ./poetry.lock ./pyproject.toml ./
ENV POETRY_VIRTUALENVS_CREATE false
RUN poetry check && poetry config --list && poetry install
COPY . .
CMD poetry run streamlit run app/app.py
