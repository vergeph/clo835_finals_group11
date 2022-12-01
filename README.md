# Install the required MySQL package

sudo apt-get update -y
sudo apt-get install mysql-client -y

# Running application locally
pip3 install -r requirements.txt
sudo python3 app.py
# Building and running 2 tier web application locally
### Building mysql docker image 
```docker build -t my_db -f Dockerfile_mysql . ```

### Building application docker image 
```docker build -t my_app -f Dockerfile . ```

### Running mysql
```docker run -d -e MYSQL_ROOT_PASSWORD=pw  my_db```


### Get the IP of the database and export it as DBHOST variable
```docker inspect <container_id>```


### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=127.0.0.1
export DBPORT=3307
```
### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=172.17.0.2
export DBPORT=3306
```
```
export DBUSER=root
export DATABASE=employees
export DBPWD=pw
export APP_BACKGROUND=back2
export S3_BUCKET=arn:aws:s3:::clo835-finals-group11
export S3_KEY=ASIAWZIDVPRD6VZXTZXT
export S3_SECRET=lnXoctgcAm2BAadjRHo1FX/2zIZsLN1JOr4COqzp
```
### Run the application, make sure it is visible in the browser
```docker run -p 81:81  -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e  DBUSER=$DBUSER -e DBPWD=$DBPWD  -e  APP_BACKGROUND=$APP_BACKGROUND -e S3_BUCKET=$S3_BUCKET -e S3_KEY=$S3_KEY -e S3_SECRET=$S3_SECRET my_app```
