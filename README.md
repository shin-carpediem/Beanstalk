<img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=flat"> <img src="https://img.shields.io/badge/-Bootstrap-563D7C.svg?logo=bootstrap&style=flat"> <img src="https://img.shields.io/badge/-Sass-CC6699.svg?logo=sass&style=flat"> <img src="https://img.shields.io/badge/-Amazon%20AWS-232F3E.svg?logo=amazon-aws&style=flat">

# Beanstalk

Technique:

- AWS lightsail(Ubuntu + Apache + gunicorn + Django)
- Pipenv
- Vue.Draggable
- MySQL

To go into virtual environment with Pipfile,

```
$ pipenv shell
```

To install package,

```
$ pipenv install hogehoge
```

To execute Pipfile each script,

```
$ pipenv run hogehoge
```

To exit from virtual environment,

```
$ exit
```

To optimize pip for lightsail,

```
pipenv lock -r > requirements.txt
```

To restart apache,

```
$ sudo /opt/bitnami/ctlscript.sh restart apache
```

https://qiita.com/CyberMergina/items/f889519e6be19c46f5f4
To enter MySQL on Lightsail,

```
$ mysql -u username -p -h endpoint
```

To exit from MySQL,

```
> exit
```

To check the Apache log

```
$ /opt/bitnami/apache2/logs/access_log
$ /opt/bitnami/apache2/logs/error_log
```
