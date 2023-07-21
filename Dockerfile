FROM python:3.10

RUN apt-get update \
    && apt-get install -y git

WORKDIR /app

COPY id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa

# Configure SSH to not prompt for confirmation when connecting to new hosts
RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

RUN git clone git@github.com:CS428-Group5/cs428-backend.git

WORKDIR /app/cs428-backend

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]