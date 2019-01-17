from continuumio/anaconda3
RUN apt update -y 
RUN apt upgrade -y 
RUN apt install gdal-bin python-gdal python3-gdal libgl1-mesa-glx -y 
RUN /opt/conda/bin/conda install numpy scipy scikit-learn docopt matplotlib geos affine gdal libiconv opencv -y
