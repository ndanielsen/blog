from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post
# Create your tests here.

class PostTest(TestCase):
	def test_create_post(self):
		post = Post()
		post.title = "My first post"
		post.text = "This is my first blog post"
		post.pub_date = timezone.now()
		post.save()

		# check we can find it

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)


		# check attributes

		self.assertEquals(only_post.title, "My first post")
		self.assertEquals(only_post.text, 'This is my first blog post')
		self.assertEquals(only_post.pub_date.day, post.pub_date.day)
		self.assertEquals(only_post.pub_date.month, post.pub_date.month)
		self.assertEquals(only_post.pub_date.year, post.pub_date.year)
		self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
		self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
		self.assertEquals(only_post.pub_date.second, post.pub_date.second)


class AdminTest(LiveServerTestCase):
	fixtures = ['users.json']


	def test_login(self):
		#create Client

		c = Client()

		#get Login page
		response = c.get('/admin/', follow=True)

		#Check response code

		self.assertEquals(response.status_code, 200)

		#check 'log in' in response
		self.assertTrue('Log in' in response.content)

		# Log the user in
		c.login(username='bobsmith', password='password')

		#Check response code
		response = c.get('/admin/')
		self.assertEquals(response.status_code, 200)

		#check log out

		self.assertTrue('Log out' in response.content)

	def test_logout(self):

		c = Client()

		c.login(username='bobsmith', password='password')

		response = c.get('/admin/')

		self.assertEquals(response.status_code, 200)

		self.assertTrue('Log out' in response.content)

		c.logout()

		response = c.get('/admin/', follow=True)

		self.assertEquals(response.status_code, 200)

		self.assertTrue('Log in' in response.content)

