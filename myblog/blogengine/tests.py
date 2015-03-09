from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import markdown2 as markdown

# Create your tests here.

class PostTest(TestCase):
	def test_create_post(self):
		
		# create the author

		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		post = Post()
		post.title = "My first post"
		post.text = "This is my first blog post"
		post.slug = "my-first-post"
		post.pub_date = timezone.now()
		post.author = author

		post.save()

		# check we can find it

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)


		# check attributes

		self.assertEquals(only_post.title, "My first post")
		self.assertEquals(only_post.text, 'This is my first blog post')
		self.assertEquals(only_post.slug, "my-first-post")

		self.assertEquals(only_post.pub_date.day, post.pub_date.day)
		self.assertEquals(only_post.pub_date.month, post.pub_date.month)
		self.assertEquals(only_post.pub_date.year, post.pub_date.year)
		self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
		self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
		self.assertEquals(only_post.pub_date.second, post.pub_date.second)

		self.assertEquals(only_post.author.username, 'testuser')
		self.assertEquals(only_post.author.email, 'user@example.com')


class BaseAcceptanceTest(LiveServerTestCase):
	def setUp(self):
		self.client = Client()


class AdminTest(BaseAcceptanceTest):
	fixtures = ['users.json']



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
			'pub_date_1': '22:00:04',
			'slug': 'my-first-post'


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

		# author = User.objects.create_user('testuser', 'user@example.com', 'password')
		# author.save()
		# post = Post()
		# post.title = 'My first post'
		# post.text = 'This is my first blog post'
		# post.pub_date = timezone.now()
		# post.author = author

		# post.save()

  #       ## Log in
		# self.client.login(username='bobsmith', password="password")


  #       # Edit the post
		# response = self.client.post('/admin/blogengine/post/2/', {
		# 	'title': 'My second post',
		# 	'text': 'This is my second blog post',
		# 	'pub_date_0': '2013-12-28',
		# 	'pub_date_1': '22:00:04',
		# 	'slug': 'my-first-post'
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

		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.slug = "my-first-post"
		post.pub_date = timezone.now()
		post.author = author
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


class PostViewTesT(BaseAcceptanceTest):


	def test_index(self):

		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		# CREATE post

		post = Post()
		post.title = 'My first post'
		post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
		post.slug = "my-first-post"
		post.pub_date = timezone.now()
		post.author = author
		post.save()

		all_posts = Post.objects.all()

		self.assertEquals(len(all_posts), 1)

		response = self.client.get("/")
		self.assertEquals(response.status_code, 200)

		self.assertTrue(post.title in response.content)

		self.assertTrue(markdown.markdown(post.text) in response.content)

		self.assertTrue(str(post.pub_date.year) in response.content)

		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)


	def test_post_page(self):
		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		# Create the post
		post = Post()
		post.title = 'My first post'
		post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
		post.slug = "my-first-post"
		post.pub_date = timezone.now()
		post.author = author
		post.save()

		# Check new post saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Get the post URL
		post_url = only_post.get_absolute_url()

		# Fetch the post
		response = self.client.get(post_url)
		self.assertEquals(response.status_code, 200)

		# Check the post title is in the response
		self.assertTrue(post.title in response.content)

		# Check the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in response.content)

		# Check the post date is in the response
		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)


class FlatPageViewTest(BaseAcceptanceTest):

	def test_create_flat_page(self):

		page = FlatPage()
		page.url = '/about/'
		page.title = 'About me'
		page.content = "All about me"
		page.save()

		page.sites.add(Site.objects.all()[0])
		page.save()


		all_pages = FlatPage.objects.all()
		self.assertEquals(len(all_pages), 1)
		only_page = all_pages[0]
		self.assertEquals(only_page, page)

		self.assertEquals(only_page.url, '/about/')
		self.assertEquals(only_page.title, 'About me')
		self.assertEquals(only_page.content, 'All about me')

		page_url = only_page.get_absolute_url()

		response = self.client.get(page_url)

		self.assertEquals(response.status_code, 200)

		# Check title and content in response
		self.assertTrue('About me' in response.content)
		self.assertTrue('All about me' in response.content)