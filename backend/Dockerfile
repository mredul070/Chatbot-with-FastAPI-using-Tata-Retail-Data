FROM python:3.11.4

WORKDIR /chatbot/app/

RUN ls -lha
COPY ./requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN ls -lha

WORKDIR /chatbot/
RUN ls -lha
COPY . .
RUN ls -lha
RUN realpath main.py
ENV PYTHONPATH=/chatbot
CMD alembic upgrade head && python main.py