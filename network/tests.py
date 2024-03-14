from django.test import Client, TestCase

from .models import User, Post, Follow


#, created_at="2023-06-24 15:38:00"    created_at="2023-06-24 15:30:00"

# Create your tests here.

class NetworkTestCase(TestCase):

    def setUp(self):
        #create users
        u1 = User.objects.create(username="ABC", password="pass")
        u2 = User.objects.create(username="DEF", password="con")
        u3 = User.objects.create(username="GHI", password="go")

        #create posts
        Post.objects.create(text="I am a programmer", user=u1)
        Post.objects.create(text="I am", user=u2)
        Post.objects.create(text="the boy is a good boy", user=u3)

        #create followers
        f1 = Follow.objects.create(follower=u1, following=u2)
        f2 = Follow.objects.create(follower=u1, following=u3)

    
    def test_valid_post(self):
        u1 = User.objects.get(username="ABC")
        p = Post.objects.get(text="I am a programmer", user=u1)
        self.assertTrue(p.is_content_valid())

    def test_invalid_post(self):
        u2 = User.objects.get(username="DEF")
        p = Post.objects.get(text="I am", user=u2)
        self.assertFalse(p.is_content_valid())

    # def test_followers_count(self):
    #     u1 = User.objects.get(username="ABC")
    #     u2 = User.objects.get(username="DEF")
    #     u3 = User.objects.get(username="GHI")

    #     f1 = Follow.objects.get(follower=u1, following=u2)
    #     #f1 = Follow.objects.get(follower=u1, following=u3)
        
    #     self.assertEqual(f1.number_of_followers(), 1)

    def test_index(self):
        c = Client()
        response = c.get("")
        self.assertEqual(response.status_code, 200)

    def test_class_ai(self):
        c = Client()
        response = c.get("/class")
        self.assertEqual(response.status_code, 200)

