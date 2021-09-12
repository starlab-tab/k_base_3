# Back

## 快速部署

```
sudo passwd
```

```
adduser knowbase && adduser knowbase sudo
```

```
sudo apt update && sudo apt upgrade -y && sudo apt install nginx -y && sudo apt install mariadb-server -y
```

```
su -- knowbase
```

### Mariadb

```
sudo mysql
```

```
alter user 'root'@'localhost' identified by 'root';
```

```
update user set user="root@?" where user="root@116.92.233.19";
```

```
CREATE DATABASE knowbase;
```

```
grant all on knowbase.* to 'root'@'192.168.44.1' identified by 'root';
```

```
use knowbase
```

```
INSERT INTO neddle (ident, auth) VALUES ('neddle', 'pbkdf2:sha256:150000$MRGHSBzO$0c430fe783e250c29ff5417893fa68b3a89ca68624bbbdee09683b0a1648416a');
```

```
flush privileges;
```

> Ubuntu comment bind-address

```
sudo gedit /etc/mysql/mariadb.conf.d/50-server.cnf
```

```
sudo systemctl restart mariadb
```

### Redis

```
sudo apt install redis-server -y
```

```
sudo gedit /etc/redis/redis.conf
```

```
requirepass
```

```
bind
```

```
sudo systemctl restart redis
```

### Deploy

```
sudo mkdir -p /opt/deployment/knowbase/frontstage/conf
```

```
sudo mkdir -p /opt/deployment/knowbase/frontstage/log
```

```
sudo mkdir -p /opt/deployment/knowbase/backstage/conf
```

```
sudo mkdir -p /opt/deployment/knowbase/backstage/log
```

```
sudo mv ~/Downloads/station /opt/deployment/knowbase/backstage
```

```
sudo mv ~/Downloads/base /opt/deployment/knowbase/frontstage
```

```
sudo mv ~/Downloads/knowbase/back/station /opt/deployment/knowbase/backstage
```

```
sudo mv ~/Downloads/knowbase/back/base /opt/deployment/knowbase/frontstage
```



```
sudo chown -R knowbase:knowbase /opt/deployment/knowbase
```

```
sudo rm -rf /opt/deployment/knowbase/frontstage/log/*
```

```
sudo rm -rf /opt/deployment/knowbase/backstage/log/*
```

### Gunicorn

```
sudo gedit /opt/deployment/knowbase/frontstage/conf/gunicorn.conf.py
```

```
sudo gedit /opt/deployment/knowbase/backstage/conf/gunicorn.conf.py
```

```
import multiprocessing
from gunicorn import glogging  

bind = '127.0.0.1:4000'

workers = multiprocessing.cpu_count() * 2 + 1

loglevel = 'info'
errorlog = '../log/error.log'
accesslog = '../log/access.log'
access_log_format = '{"time": "%(t)s", "ip": "%({X-Real-IP}i)s", "xff": "%({X-Forwarded-For}i)s", "url": "%(r)s", "code": "%(s)s", "resp_len": "%(b)s", "agent": "%(a)s"}'
glogging.Logger.error_fmt = '{"time": "%(asctime)s", "file": "%(module)s", "line_num": "%(lineno)d", "msg": "%(message)s", "level": "%(levelname)s"}'
```

### Miniconda

```
sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 -y
```

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

```
bash ~/Downloads/Miniconda3-latest-Linux-x86_64.sh
```

```
export PATH=$PATH:/home/knowbase/miniconda3/bin
```

```
source ~/.bashrc
```

```
conda create -n knowbase python=3.8.8
```

```
conda activate knowbase
```

```
conda env list
```

```
conda info -e
```

```
pip install -r ~/Downloads/requestments.txt
```

```
WTForms==2.3.3
Flask==1.1.2
flask_caching==1.10.1
Flask_JWT_Extended==4.1.0
flask_marshmallow==0.14.0
Flask_SQLAlchemy==2.5.1
SQLAlchemy==1.3.23
cryptography==3.4.7
marshmallow==3.11.1
marshmallow-sqlalchemy==0.24.2
requests==2.25.1
Werkzeug==1.0.1
pyotp==2.6.0
pymysql==1.0.2
Flask_Cors==3.0.10
beautifulsoup4==4.9.3
lxml==4.6.3
Pillow==8.2.0
gunicorn==20.1.0
pysocks==1.7.1
flask-redis==0.4.0
markdown==3.3.4
```

### Supervisor


```
sudo apt install supervisor
```

```
sudo gedit /etc/supervisor/conf.d/gunicorn_backstage.conf
```

```
sudo gedit /etc/supervisor/conf.d/gunicorn_frontstage.conf
```

```
[program:gunicorn_backstage]

command=/home/knowbase/miniconda3/envs/knowbase/bin/gunicorn serve:app -c /opt/deployment/knowbase/backstage/conf/gunicorn.conf.py

directory=/opt/deployment/knowbase/backstage/station

user=knowbase
autostart=no
autorestart=true

stdout_logfile = /opt/deployment/knowbase/backstage/log/super_gnc_std.log
stderr_logfile = /opt/deployment/knowbase/backstage/log/super_err.log
```

```
[program:gunicorn_frontstage]

command=/home/knowbase/miniconda3/envs/knowbase/bin/gunicorn serve:app -c /opt/deployment/knowbase/frontstage/conf/gunicorn.conf.py

directory=/opt/deployment/knowbase/frontstage/base

user=knowbase
autostart=no
autorestart=true

stdout_logfile = /opt/deployment/knowbase/frontstage/log/super_gnc_std.log
stderr_logfile = /opt/deployment/knowbase/frontstage/log/super_err.log
```

```
mkdir /var/run/mydaemon
chown myuser:myuser /var/run/mydaemon
```

```
sudo supervisorctl reread
```

```
sudo supervisorctl update
```

```
sudo supervisorctl start gunicorn_backstage
```

```
sudo supervisorctl start gunicorn_frontstage
```

### Nginx

```
限制nginx目录
```

```
sudo nano /etc/nginx/nginx.conf
```

```
sudo nano /etc/nginx/conf.d/knowbase.conf
```

```
upstream frontstage {
	server localhost:5000;
}
upstream baskstage{
	server localhost:4000;
}

server {
	
	listen  80;
        server_name    localhost;
        root    /usr/share/nginx/html;
        location / {
                index   index.html;
                try_files $uri $uri/ /index.html;
        }
        location /media/ {
		root    /usr/share/nginx;
        }
        location /kapi/ {
	        proxy_pass http://frontstage/v2/;
	        proxy_redirect off;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		# proxy_set_header X-Forwarded-Host $server_name;
        }
}

server {
	
	listen  8000;
        server_name    localhost;
		root    /var/www/html;
        location /valardohaeris/ {
                try_files $uri $uri/ /valardohaeris/index.html;
        }
        location /media/ {
		root    /usr/share/nginx;
        }
        location /m2/ {
		proxy_pass http://baskstage;
		proxy_redirect off;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		client_max_body_size 10M;
        }
}
```

```
publicPath: '/valardohaeris/',
```

```
sudo systemctl restart nginx
```

```
sudo mkdir /usr/share/nginx/media
```

```
sudo chmod -R a+r /usr/share/nginx/media
```

```
sudo chown -R knowbase:knowbase /usr/share/nginx/media
```

```
sudo rm -rf /usr/share/nginx/html/*
```

```
sudo rm -rf /var/www/html/valardohaeris/*
```

```
sudo mkdir -p /usr/share/nginx/html
```

```
sudo mkdir -p /var/www/html/valardohaeris
```

```
sudo mv ~/Downloads/dist/* /usr/share/nginx/html
```

```
sudo mv ~/Downloads/dist/* /var/www/html/valardohaeris
```

```
sudo mv ~/Downloads/knowbase/front/dist-front/* /usr/share/nginx/html
```

```
sudo mv ~/Downloads/knowbase/front/dist-back/* /var/www/html/valardohaeris
```

### UFW

```
sudo ufw enable
```

```
sudo ufw allow 80
```

```
sudo ufw allow from 192.168.44.1 to any port 3306
```

```
There's an implicit "deny from all" (inbound) when using UFW, so you don't need to add a rule to do that. (And also an implicit "allow all outbound".)
```

```
sudo rm -rf /opt/deployment/knowbase/frontstage/log/*
```

```
sudo rm -rf /opt/deployment/knowbase/backstage/log/*
```

# Front-Base

```
vue create knowbase
```

```
cd knowbase
```

```
vue add vuetify
```

```
vue add style-resources-loader
```

```
cnpm install @mdi/font -D
```

```
import '@mdi/font/css/materialdesignicons.css'

export default new Vuetify({
  icons: {
    iconfont: 'mdi',
  },
});
```

```
cnpm install axios -S
```

```
cnpm install viewerjs -S
```

```
cnpm install dompurify -S
```

```
cnpm install vue-masonry -S
```

```
cnpm install vuetify-dialog -S
```

# Front-Station

```
vue create kbstation
```

```
cd kbstation
```

```
vue add vuetify
```

```
Choose a preset: Default (recommended)
```

```
vue add style-resources-loader
```

```
cnpm install @mdi/font -D
```

```
import '@mdi/font/css/materialdesignicons.css'

export default new Vuetify({
  icons: {
    iconfont: 'mdi',
  },
});
```

```
cnpm install axios -S
```

```
cnpm install promise.prototype.finally -S
```

```
cnpm i @kangc/v-md-editor -S
```

```
cnpm install dompurify -S
```

```
cnpm install js-beautify -S
```

```
cnpm install jsonlint -S
```

```
cnpm install marked -S
```

```
cnpm install node-forge -S
```

```
const forgePlugn = {
    install(Vue) {
        Vue.prototype.$forge = forge;
    }
}
Vue.use(forgePlugn);
```

```
cnpm install vuetify-dialog -S
```

```
cnpm install  -S
```

```\
sudo apt-get install vsftpd -y	&& sudo apt-get install ssh
sudo nano /etc/vsftpd.conf


vsftpd_log_file=/var/log/vsftpd.log
listen_port=6633
pasv_enable=Yes
pasv_min_port=50000
pasv_max_port=50100
allow_writeable_chroot=NO
user_sub_token=$USER
local_root=/home/$USER/ftp
userlist_enable=YES
userlist_file=/etc/vsftpd.user_list
userlist_deny=NO

sudo nano /etc/vsftpd.user_list

sudo useradd -m -s /bin/bash ksftp
sudo passwd ksftp
bc43f8D_33Z2b
sudo mkdir /home/ksftp/ftp
sudo chown nobody:nogroup /home/ksftp/ftp
sudo chmod a-w /home/ksftp/ftp
sudo mkdir /home/ksftp/ftp/files
sudo chown -R ksftp:ksftp /home/ksftp/ftp/files
sudo chmod -R 0770 /home/ksftp/ftp/files

sudo ufw allow 50000:50100/tcp

sudo systemctl restart vsftpd
sudo systemctl status vsftpd

sudo ufw allow from any to any port 21
sudo ufw status

sudo ufw reload

sudo /home/ksftp/ftp/files/station /home/knowbase/Downloads
sudo mv /home/ksftp/ftp/files/station /home/knowbase/Downloads
sudo nano /etc/ssh/sshd_config
sudo systemctl restart ssh
sudo systemctl status ssh
sudo nano /etc/ssh/sshd_config
```

```
sudo nano /etc/ssh/sshd_config
```

```
Port 7742
```

```
AllowUsers	knowbase
```

```
sudo ufw allow 7742
```