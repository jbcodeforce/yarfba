
# A CDK for a ALB to ECS Fargate to a Flask app


The Flask app back-end run within a Flask container on Fargate. The app will be part of a target group of an ALB. All within a new VPC.

To test the Flask app locally:

```sh
cd server
pip install -r requirements.txt
python app.py
```

In web browser go to [localhost](http://localhost/) to get the Hello world and use one of the api

* [/reverse/<astring>](http://localhost/reverse/tuesbelletoi)
* [/health]((http://localhost/health)

To build a docker image from server folder:

```
docker build -t 
```