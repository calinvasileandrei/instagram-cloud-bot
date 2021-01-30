FROM python:alpine3.9
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
#EXPOSE 5000
ENV auth_username=user_for_auth
ENV auth_password=pass_for_auth
ENV username=insta_user
ENV password=insta_pass
CMD python3 ./main.py