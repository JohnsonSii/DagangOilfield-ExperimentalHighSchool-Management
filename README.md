# 大港油田实验中学新生审核管理系统

## 项目初始化

```python
# djangoServer/djangoServer/settings.py

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "",  # 你的 MySQL 数据库名称
        "USER": "",  # 你的数据库用户名
        "PASSWORD": "",  # 你的数据库密码
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

## 后端运行

````bash
# 替换为你自己的 SSL 证书
python manage.py runsslserver --addrport 8080 --certificate .\crt\your-certification.pem --key .\crt\your-certification.key
````

## Uni App 前端打包

### 推荐使用 HBuilder 发行

![image](https://github.com/JohnsonSii/DagangOilfield-ExperimentalHighSchool-Management/assets/67853082/d1b095fa-2fcf-4e9b-a8b4-4d4f323c04a4)

### NPM 打包

```bash
npm run build:h5
```

## 前端部署

打包完毕将生成一个 `h5` 文件夹，将其放到合适的位置，如 Windows 系统 `C:/www/xxx.com` 或 Linux 系统 `/www/xxx.com`

### Nginx 部署配置

```bash
server {
        listen       9000;
        server_name  xxx.com;  # 此处填写你的域名
        

        location / {
            root      C:/www/xxx.com;  # 此处填写 h5 文件夹路径
            index     index.html;
            try_files $uri $uri/ /index.html;
        }

    }
    
# HTTPS server
    
server {
    listen       9443 ssl;
    server_name  xxx.com;  # 此处填写你的域名

    ssl_certificate C:/src/nginx-1.24.0/certs/your-certification.pem;  # 此处填写你的证书路径
    ssl_certificate_key C:/src/nginx-1.24.0/certs/your-certification.key;  # 此处填写你的证书密钥路径

    location / {
        root      C:/www/xxx.com;  # 此处填写 h5 文件夹路径
        index     index.html;
        try_files $uri $uri/ /index.html;
    }
}
```



## 项目展示图

![image](https://github.com/JohnsonSii/DagangOilfield-ExperimentalHighSchool-Management/assets/67853082/a89873e8-60e4-49f1-a376-b2a063943b3f)

![image](https://github.com/JohnsonSii/DagangOilfield-ExperimentalHighSchool-Management/assets/67853082/dd31983d-837a-4881-99a5-9c17ddcc2e56)

![image](https://github.com/JohnsonSii/DagangOilfield-ExperimentalHighSchool-Management/assets/67853082/3741dfca-955c-4ace-bf81-908d2ee6ff9e)
