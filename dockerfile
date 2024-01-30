FROM python:3.12-slim
ENV APP_HOME /code
WORKDIR $APP_HOME
COPY . ./
RUN pip install -r requirements.txt
CMD exec python main.py