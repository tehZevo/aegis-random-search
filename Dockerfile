FROM python:3.9

WORKDIR /app

#https://github.com/gabrieldemarmiesse/python-on-whales/blob/master/docs/template/user_guide/running_python_on_whales_inside_a_container.md
RUN mkdir -p ~/.docker/cli-plugins/
RUN wget https://github.com/docker/buildx/releases/download/v0.6.3/buildx-v0.6.3.linux-amd64 -O ~/.docker/cli-plugins/docker-buildx
RUN chmod a+x  ~/.docker/cli-plugins/docker-buildx

RUN mkdir -p ~/.docker/cli-plugins/
RUN wget https://github.com/docker/compose/releases/download/v2.0.1/docker-compose-linux-x86_64 -O ~/.docker/cli-plugins/docker-compose
RUN chmod a+x  ~/.docker/cli-plugins/docker-compose

COPY requirements.txt ./

# RUN apk add git
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD [ "python", "-u", "main.py" ]
