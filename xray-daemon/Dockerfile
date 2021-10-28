FROM amazonlinux:2

RUN yum install -y unzip
RUN curl -o daemon.zip https://s3.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-linux-3.x.zip
RUN unzip daemon.zip && cp xray /usr/local/bin/xray

EXPOSE 2000/udp
EXPOSE 2000/tcp

ENTRYPOINT ["/usr/local/bin/xray", "-t", "0.0.0.0:2000", "-b", "0.0.0.0:2000"]
CMD ["-o"]
