from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post, Comment
from rest_framework.test import APIClient

class PostAPITestCase(APITestCase):
    
    def setUp(self):
        """
        Set up test data: create users, posts, and comments.
        """
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        
        # Create some posts
        self.post1 = Post.objects.create(text='Post 1 text', user=self.user1)
        self.post2 = Post.objects.create(text='Post 2 text', user=self.user2)

        # Create some comments
        Comment.objects.create(text='Comment 1 for Post 1', post=self.post1, user=self.user2)
        Comment.objects.create(text='Comment 2 for Post 1', post=self.post1, user=self.user1)
        Comment.objects.create(text='Comment 3 for Post 1', post=self.post1, user=self.user2)
        Comment.objects.create(text='Comment 1 for Post 2', post=self.post2, user=self.user1)

    def test_post_list_api(self):
        """
        Test the Post list API endpoint
        """
        client = APIClient()
        response = client.get('/posts/') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        data = response.data
        self.assertIn('results', data)  # Ensure the response contains 'results'
        self.assertTrue(len(data['results']) > 0)  # Ensure that there is at least one post in the response

        # Check for expected fields in the response (comment count, user, etc.)
        post_data = data['results'][0]  # Access the first post from the 'results' list
        self.assertIn('id', post_data)
        self.assertIn('text', post_data)
        self.assertIn('timestamp', post_data)
        self.assertIn('user', post_data)
        self.assertIn('comment_count', post_data)

        # Check comments for a post (should be up to 3 random comments)
        self.assertIn('comments', post_data)
        self.assertTrue(len(post_data['comments']) <= 3)  # Ensure no more than 3 comments


    def test_pagination(self):
        """
        Test the pagination of the Post list API endpoint
        """
        client = APIClient()
        response = client.get('/posts/?page=1&page_size=2')  # You can modify the pagination size if needed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data['results']), 2)  # Ensure we only get 2 posts in the response

    def test_comment_count(self):
        """
        Test that the correct comment count is returned for each post
        """
        client = APIClient()
        response = client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        for post in data['results']:
            post_id = post['id']
            post_obj = Post.objects.get(id=post_id)
            self.assertEqual(post['comment_count'], post_obj.comments.count())

    def test_post_ordering(self):
        """
        Test that posts are ordered by timestamp in descending order
        """
        client = APIClient()
        response = client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data['results']
        timestamps = [post['timestamp'] for post in data]
        self.assertEqual(timestamps, sorted(timestamps, reverse=True))  # Ensure posts are sorted latest first

    def test_post_with_no_comments(self):
        """
        Test that posts with no comments are handled correctly
        """
        client = APIClient()

        # Create a post with no comments
        post_no_comments = Post.objects.create(text='Post with no comments', user=self.user1)

        response = client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        post_data = next(post for post in data['results'] if post['id'] == str(post_no_comments.id))
        
        # Ensure the post has no comments
        self.assertEqual(post_data['comment_count'], 0)
        self.assertEqual(len(post_data['comments']), 0)

    