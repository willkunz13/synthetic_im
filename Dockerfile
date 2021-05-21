FROM python:latest
COPY . /app
WORKDIR /app
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y vim
RUN pip install . --no-cache-dir
RUN pip uninstall -y synthetic_im
CMD ["waitress-serve", "app:app"]
