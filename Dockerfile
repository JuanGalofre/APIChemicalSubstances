FROM python:3.12.1
WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn
COPY . .

CMD  ["uvicorn", "AppAlch.main:app" ,"--host","0.0.0.0","--port","8000"] 

ENV PATH="/usr/src/app:${PATH}"
