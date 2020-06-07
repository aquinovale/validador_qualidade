FROM webysther/aws-glue:spark-1.0-py3

COPY src ./
COPY resource ./

USER root
RUN apt-get -q update -y && \
	apt-get -qq install -y libpq-dev gcc mdbtools && \
	rm -rf /var/lib/apt/lists/*


RUN python -m pip install colorama docutils futures jmespath numpy pandas pip pyasn1
RUN python -m pip install pygresql python-dateutil pytz pyyaml rsa s3transfer 
RUN python -m pip install scikit-learn scipy setuptools six virtualenv wheel
RUN python -m pip install jellyfish pandas_profiling python-magic xlrd unidecode pandas_access

RUN mkdir /tmp/output
RUN mkdir /tmp/validador

RUN chown -R docker:docker /opt
RUN chown -R docker:docker /usr/local
RUN chown -R docker:docker /tmp/validador
RUN chown -R docker:docker /tmp/output

USER docker
