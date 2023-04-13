# 0. requirements

- docker installed
- docker-compose installed
- python 3.8.2 installed

Run the project on Mac OS X or Linux.

# 1.Quickstart

If you want to configure the rate of the flask worker, update RATE ( records / sec ) variable in .env file  

### 1.1. Start the db service

Open a terminal and run the following command in the root directory of the project:
```
docker-compose up db
```

Wait 1 minute until the db service is up and running. 

### 1.2. Init the db

Open a terminal and run the following command in the root directory of the project:
```
docker-compose run --rm flask_worker flask db upgrade
 ```

It will create tables used by the app.

### 1.3. Start the flask worker and flask web app
Open a terminal and run the following command in the root directory of the project:
```
docker-compose up 
```
Wait a few minutes until the flask worker is sending data to the db.

### 1.4. Check that flask worker is sending data to the db

Open a terminal and run the following command in the root directory of the project:
```
docker-compose logs -f flask_worker
```

### 1.5. Query the flask api to get individual records

Open a terminal and run the following command in the root directory of the project:
```
curl --location --request GET 'http://127.0.0.1:5000/videos?limit=20&offset=0'
```

### 1.6. Query the flask api to get aggregated records
Open a terminal and run the following command in the root directory of the project:
```
curl --location --request GET 'http://127.0.0.1:5000/videos/agg?operation=sum&field=views,likes,dislikes'
```

To get the doc api, open a browser and go to [API documentation](https://documenter.getpostman.com/view/26721070/2s93RXqptg)

