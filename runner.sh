# Runner for docker container
docker run -it -p 8000-8010:8000-8010 -p 6006-6010:6006-6010 --cpus=8 -m 2G -v $PWD/cpu_usage:/app/cpu_usage/ soheilzi/comp_livetune:v2 bash