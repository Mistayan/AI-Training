FROM python:3.12-alpine as update
RUN apk udpdate; apk upgrade
RUN apk add git
WORKDIR /home/app


FROM update as pytactx
RUN git clone --recurse-submodule --depth 1 https://github.com/jusdeliens/pytactx


FROM pytactx as install_requirements
ADD src/bot_de_course/requirements.txt .
RUN pip install -r requirements.txt; rm requirements.txt


FROM install_requirements as copy_src
RUN mkdir src; mkdir src/bot_de_course
ADD src/utils ./src/utils
ADD src/bot_de_course/*.py ./src/bot_de_course
ADD race.py .
ADD config.py .


FROM copy_src as runner
CMD ["python", "race.py"]