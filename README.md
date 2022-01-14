# Twitter_Data_Pipeline

![twitter_pipeline.png](twitter_pipeline.png)


This pipeline collects tweets accroding to a specific buzzword, does a simple sentiment analysis for each tweet and stores it into a database.

### How to use

* Note: You need to have docker installed in order to run this pipeline.

In the file `get_tweets.py` search for the line `listener = MaxTweetsListener(max_tweets=20)` to set the maximal number of tweets you want to collect and search for the line `stream.filter(track=['Covid'], languages=['en'], is_async=False)` to set the buzzword you want to track and the tweet language.

To build the docker images for the pipeline type `sudo docker-compose build` as a bash command at the directory where you store the file `docker-compose.yml`. Docker creates now a virtual machine on which it installs Python 3.6 and all imports from the `requirements.txt` files.

To run the docker containers type `sudo docker-compose up` and your pipeline starts running`.

* Note: If your are using MacOS you can skip the sudo command.

