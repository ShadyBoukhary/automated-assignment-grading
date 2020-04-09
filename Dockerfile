FROM kennethreitz/pipenv as pipenv

ADD . /app
WORKDIR /app
RUN pwd
RUN ls -lhas

RUN pipenv install --dev \
 && pipenv lock -r > requirements.txt \
 && pipenv run python setup.py bdist_wheel

# ----------------------------------------------------------------------------
FROM ubuntu:bionic

ARG DEBIAN_FRONTEND=noninteractive

COPY --from=pipenv /app/dist/*.whl .

RUN set -xe \
 add-apt-repository ppa:george-edison55/cmake-3.1 \
 && apt-get update -q \
 && apt-get install -y -q \
        python3-minimal \
        python3-wheel \
        python3-pip \
        vim \
        bash \
        git-core \
        build-essential \
        cmake \
 && apt-get -y upgrade \
 && python3 -m pip install *.whl \
 && apt-get remove -y python3-pip python3-wheel \
 && apt-get autoremove -y \
 && apt-get clean -y \
 && rm -f *.whl \
 && rm -rf /root/.cache \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /app \
 && useradd aaa_user --user-group

RUN mkdir /app/shared/ \
 && touch /app/shared/assignment_list.json \
 && ln -s /usr/local/lib/python3.6/dist-packages/aaa /app/aaa \
 && export alias grader="python3 /usr/local/lib/python3.6/dist-packages/aaa" \
 && mkdir /home/aaa_user \
 && echo 'alias grader="python3 /usr/local/lib/python3.6/dist-packages/aaa"' >> /home/aaa_user/.bashrc \
 #&& chown aaa_user /home/aaa_user/.bashrc
 && chown -R aaa_user /home/aaa_user \
 && chown -R aaa_user /app/

COPY ./shared/CMakeLists.txt /app/shared/CMakeLists.txt
RUN chown aaa_user app/shared/CMakeLists.txt
USER aaa_user
ENV DEBUG FALSE
ENV PATH="/usr/local/lib/python3.6/dist-packages/:${PATH}"
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV DEV FALSE
ENV SHARED "/app/shared/"
WORKDIR /app

#RUN mkdir -p /home/aaa_user/resources

#ENTRYPOINT ["python3", "/usr/local/lib/python3.6/dist-packages/aaa"]