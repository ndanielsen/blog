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

	def setUp(self):
		self.client = Client()


	def test_login(self):
		#create Client

		

		#get Login page
		response = self.client.get('/admin/', follow=True)

		#Check response code

		self.assertEquals(response.status_code, 200)

		#check 'log in' in response
		self.assertTrue('Log in' in response.content)

		# Log the user in
		self.client.login(username='bobsmith', password='password')

		#Check response code
		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)

		#check log out

		self.assertTrue('Log out' in response.content)

	def test_logout(self):

		#c = Client()

		self.client.login(username='bobsmith', password='password')

		response = self.client.get('/admin/')

		self.assertEquals(response.status_code, 200)

		self.assertTrue('Log out' in response.content)

		self.client.logout()

		response = self.client.get('/admin/', follow=True)

		self.assertEquals(response.status_code, 200)

		self.assertTrue('Log in' in response.content)


	def test_create_post(self):

		#log in

		self.client.login(username="bobsmith", password="password")

		#check response code

		response = self.client.get('/admin/blogengine/post/add/')

		self.assertEquals(response.status_code, 200)


	def test_create_post(self):
		#log in

		self.client.login(username="bobsmith", password="password")

		# check response code

		response = self.client.get('/admin/blogengine/post/add/')
		self.assertEquals(response.status_code, 200)

		#Create new post

		response = self.client.post('/admin/blogengine/post/add/', {
			'title': "My first post",
			'text' : "This is my first post",
			'pub_date_0': '2015-03-05',
			'pub_date_1': '22:00:04'

		},
		follow=True
		)
		self.assertEquals(response.status_code, 200)

		# Check added successfully

		self.assertTrue('added successfully' in response.content)

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

	def test_edit_post(self):
		"""
		Need to figure out how to get the post id
		"""	


		pass
		# post = Post()
		# post.title = 'My first post'
		# post.text = 'This is my first blog post'
		# post.pub_date = timezone.now()
		# post.save()

  #       ## Log in
		# self.client.login(username='bobsmith', password="password")


  #       # Edit the post
		# response = self.client.post('/admin/blogengine/post/2/', {
		# 	'title': 'My second post',
		# 	'text': 'This is my second blog post',
		# 	'pub_date_0': '2013-12-28',
		# 	'pub_date_1': '22:00:04',
		# },
		# follow=True
		# )
		# self.assertEquals(response.status_code, 200)

		# # Check changed successfully
		# self.assertTrue('changed successfully' in response.content)


		# all_posts = Post.objects.all()
		# self.assertEquals(len(all_posts), 1)
		# only_post = all_posts[0]
		# self.assertEquals(only_post.title, 'My second post')
		# self.assertEquals(only_post.text, 'This is my second blog post')

	def test_delete_post(self):

		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.pub_date = timezone.now()
		post.save()

		all_posts = Post.objects.all()
		
		self.assertEquals(len(all_posts), 1)

		self.client.login(username='bobsmith', password="password")

		# Delete the post
		response = self.client.post('/admin/blogengine/post/2/delete/', {
			'post': 'yes'
		}, follow=True)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('deleted successfully' in response.content)

		all_posts = Post.objects.all()

		self.assertEquals(len(all_posts), 0)


class PostViewTesT(LiveServerTestCase):
	def setUp(self):
		self.client = Client()

	def test_index(self):
		# CREATE post

		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.pub_date = timezone.now()
		post.save()

		all_posts = Post.objects.all()

		self.assertEquals(len(all_posts), 1)

		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)
