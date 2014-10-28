FROM    python:2.7
ADD     . /code
WORKDIR /code
ENV DEBIAN_FRONTEND noninteractive
RUN 	apt-get update
RUN 	apt-get install --fix-missing
RUN 	apt-get -y install default-jre
RUN 	apt-get -y install default-jdk
RUN     pip install -r requirements.txt
RUN 	mkdir /user
ENV		HOME 		/user
RUN 	python -m nltk.downloader -d $HOME/nltk_data all
