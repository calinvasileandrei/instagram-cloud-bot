git pull &&
sudo docker build -t instagram_cloud_bot . &&
sudo docker run -d -p 5000:5000 --name instagram_cloud_bot instagram_cloud_bot
