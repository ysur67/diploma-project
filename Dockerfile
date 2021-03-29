FROM python:3.6.9

RUN apt update

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./conf/requirements.txt .

COPY entrypoint.sh .

RUN pip3 install -r requirements.txt

RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]

CMD ['gulp', 'watch']