FROM python:3.7-slim

# set up directory
COPY . /app

# change work directory
WORKDIR /app

# install requirements
RUN pip install --upgrade -r requirements.txt

# make entrypoint executable
RUN chmod +x Entrypoint.sh

CMD ["./Entrypoint.sh"]
