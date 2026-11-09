FROM python:3.12-slim-trixie

RUN apt-get update
# RUN apt-get install -y --fix-missing wget

# RUN echo "deb https://notesalexp.org/tesseract-ocr5/$(lsb_release -cs)/ $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/notesalexp.list > /dev/null
# RUN curl -o - https://notesalexp.org/debian/alexp_key.asc | apt-key add -

# RUN apt-get update

RUN apt-get install -y tesseract-ocr tesseract-ocr-fra

RUN useradd -ms /bin/bash ndf
USER ndf

WORKDIR /app
COPY . /app

RUN pip install --editable .