FROM python:3.12
EXPOSE 5000
WORKDIR /app
# COPY requirements.txt sperately caches requirements in such
# a way that, it won't have to rerun everytime you change other 
# parts of the code, also with pip install.
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

