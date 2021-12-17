FROM centos:7
ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]

RUN set -x \
	&& yum -y install wget libXdamage libXcomposite libXrandr  mesa-libGL.x86_64 atk nss at-spi2-atk cups-libs mesa-libgbm alsa-lib git \
	&& yum groupinstall "fonts" -y \
	&& yum -y install zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel gcc make \
	&& cd ~/ \
	&& mkdir python \
	&& cd python  \
	&& wget https://mirrors.huaweicloud.com/python/3.7.7/Python-3.7.7.tgz  \
	&& tar -xvf Python-3.7.7.tgz \
	&& cd Python-3.7.7 \
	&& ./configure --prefix=/usr/local/python3 \
	&& make \
	&& make install \
	&& echo "export PATH=$PATH:/usr/local/python3/bin">>~/.bashrc \
	&& source ~/.bashrc \
	&& pip3 install --upgrade pip \
	&& pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple selenium psutil func_timeout requests urllib3 pillow websockets numpy pyyaml opencv-python \
	&& yum install chromium chromedriver \
	&& cd /home/ \
	&& git clone https://gitee.com/xxsc/JDMemberCloseAccount.git \
	&& cd JDMemberCloseAccount
ENTRYPOINT ["./docker/docker-entrypoint.sh"]
	
	