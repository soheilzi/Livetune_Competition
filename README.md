# Livetune_Competition
For people with mac os please make a conda environment and run:

conda env create -f environment.yml

to run the docker container with our settings please navigate to the root of this folder and type:
docker run -it -p 8000-8010:8000-8010 -p 6006-6010:6006-6010 --cpus=8 -m 2G -v $PWD/cpu_usage:/app/cpu_usage/ soheilzi/comp_livetune:v2
