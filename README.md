<img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=flat"> <img src="https://img.shields.io/badge/-Bootstrap-563D7C.svg?logo=bootstrap&style=flat"> <img src="https://img.shields.io/badge/-Sass-CC6699.svg?logo=sass&style=flat"> <img src="https://img.shields.io/badge/-Google%20Cloud-EEE.svg?logo=google-cloud&style=flat">

# beanstalk

Technology:

- App Engine
- Cloud SQL/MySQL
- Cloud Storage

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

To check the Apache log,

```
$ /opt/bitnami/apache2/logs/access_log
```

```
$ /opt/bitnami/apache2/logs/error_log
```

### Google Cloud Platform

https://cloud.google.com/python/django/appengine?hl=ja#creating_a_cloud_sql_instance
To deploy, access to the CloudSQL/MySQL from local

```
$ python manage.py collectstatic
```

```
$ ./cloud_sql_proxy -instances="hoge:hoge:hoge"=tcp:3306
```

debug=False and switch database from SQlite3 to MySQL, then

```
$ python manage.py makemigrations
```

```
$ python manage.py migrate
```

```
$ gcloud app deploy
```

```
$ gcloud app browse
```

To exit from CloudSQL/MySQL,

```
> quit
```
