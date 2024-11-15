from rest_framework.test import APITestCase
from . import models
from users.models import User

class TestTweets(APITestCase):
    
    PAYLOAD = "Tweet Test"
    URL = "/api/v1/tweets/"
    
    def setUp(self): 
        self.user = User.objects.create(username="hugo")
        models.Tweet.objects.create(
            payload=self.PAYLOAD,
            user=self.user,
        )
    
    def test_all_tweets(self):
        response = self.client.get(self.URL)  # client simulates CRUD and logins, etc
        data = response.json()  # Django creates and deletes a DB only for testing
        
        self.assertEqual(response.status_code, 200, "Status code isn't 200")
        self.assertEqual(data[0]["payload"], self.PAYLOAD)

    def test_create_tweet(self):
        new_tweet_payload = "New Tweet"
        
        response = self.client.post(self.URL, data={"payload": new_tweet_payload})
        data = response.json()
        
        self.assertEqual(response.status_code, 200, "Not 200 Status Code")
        self.assertEqual(data["payload"], new_tweet_payload)


class TestTweet(APITestCase):
    
    PAYLOAD = "Tweet Test"
    URL = "/api/v1/tweets/"
    
    def setUp(self): 
        self.user = User.objects.create(username="hugo")
        self.tweet = models.Tweet.objects.create(
            payload=self.PAYLOAD,
            user=self.user,
        )
        
    def test_tweet_not_found(self):
        response = self.client.get(self.URL + "2123")
        self.assertEqual(response.status_code, 404)
        
    def test_get_tweet(self):
        response = self.client.get(f"{self.URL}{self.tweet.id}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["payload"], self.PAYLOAD)
        
    def test_put_tweet(self):
        updated_tweet_payload = "Updated Tweet"
        
        response = self.client.put(
            f"{self.URL}{self.tweet.id}",
            data={"payload": updated_tweet_payload},
            content_type="application/json",
        )
        data = response.json()
        
        self.assertEqual(response.status_code, 200, "Not 200 Status Code")
        self.assertEqual(data["payload"], updated_tweet_payload)
    
    def test_delete_tweet(self):
        response = self.client.delete(f"{self.URL}{self.tweet.id}")
        self.assertEqual(response.status_code, 204)
