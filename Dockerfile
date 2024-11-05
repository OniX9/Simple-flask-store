FROM python:3.12
# EXPOSE 5000 # Remove "EXPOSE 5000" since gunicorn would run on port 80
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt #Use the cmd line above instead, 
# prevents pip from using the cached outdated package.
COPY . .
# CMD ["flask", "run", "--host", "0.0.0.0"] # Not efficient
CMD ["/bin/bash", "docker-entrypoint.sh"]
