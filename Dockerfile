FROM python:3.11.4

WORKDIR /inventory_management/app/

RUN ls -lha
COPY ./app/requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN ls -lha

WORKDIR /inventory_management/
RUN ls -lha
COPY . .
RUN ls -lha
RUN realpath main.py
ENV PYTHONPATH=/inventory_management
CMD alembic upgrade head && python main.py