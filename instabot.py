import requests , urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


#This is the access token for the instagram API
APP_ACCESS_TOKEN = '286308105.a90ec70.7691dca881004b60b57db1cc85505c1e'

#Token owner = shefaliyadv
#Sandbox users = insta.bot.test.0, insta.bot.test.1, instabotmriutest0

BASE_URL = 'https://api.instagram.com/v1/'


#Function that retrives the value of your own instagram account. like followers, lift of followings, number of posts, etc.

def self_info():
  request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:

      if len(user_info['data']):
          print 'Username: %s' % (user_info['data']['username'])
          print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
          print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
          print 'No. of posts: %s' % (user_info['data']['counts']['media'])
      else:
          print 'User does not exist!'

  else:
      print 'Status code other than 200 received!'


#Function declaration to get the id of the user.

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None

    else:
        print 'Status code other than 200 received!'
        exit()


#Function declaration to get the info of a user by username

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)

    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'

    else:
        print 'Status code other than 200 received!'


#Function declaration to get the recent post of your own account.

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:

        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'

    else:
        print 'Status code other than 200 received!'


#Function declaration to get the recent post of another user

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:

        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'

    else:
        print 'Status code other than 200 received!'


#Function declaration to get the post id of another user's recent post.

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:

        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()

    else:
        print 'Status code other than 200 received!'
        exit()


#Function declarartion to post a like on the user's media.

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


#Function declaration to post a comment on a user's media

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)
    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


# Function declaration to delete negative comments from a user's post.

def delete_negative_comment(insta_username):
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  comment_info = requests.get(request_url).json()

  if comment_info['meta']['code'] == 200:

    if len(comment_info['data']):

        for x in range(0, len(comment_info['data'])):
            comment_id = comment_info['data'][x]['id']
            comment_text = comment_info['data'][x]['text']
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

            if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                print 'Negative comment : %s' % (comment_text)
                delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                media_id, comment_id, APP_ACCESS_TOKEN)

                print 'DELETE request url : %s' % (delete_url)
                delete_info = requests.delete(delete_url).json()

                if delete_info['meta']['code']== 200:
                    print 'Comment successfully deleted!\n'
                else:
                    print 'Unable to delete comment!'

            else:
                print 'Positive comment: %s\n' % (comment_info)

    else:
        print "There are no comments on this post."

  else:
      print 'Status code other than 200 received!'


#Function declaration to get a list of the likers for a particular post.

def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (media_id)
    print 'GET request url : %s' % (request_url)
    list_of_likes_info = requests.get(request_url).json()

    if list_of_likes_info ['meta']['code'] == 200:

        if len(list_of_likes_info['data']):
            print 'list of likes is %s' % (media_id['data'][0])
        else:
            print 'likes does not exist.'

    else:
        print 'status code other than 200 received.'


#Function declaration to get the comment list from the user's post.

def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (media_id)
    print 'GET request url : %s' % (request_url)
    list_of_comments_info = requests.get(request_url).json()
    if list_of_comments_info['meta']['data'] == 200:

        if len(list_of_comments_info['data']):
            print 'list of comments is %s' % (media_id['data'][0])
        else:
            print 'comments does not exist.'

    else:
        print 'status code other than 200 received.'


#Function declarartion to run the bot.

def start_bot():

    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.Exit"

        choice=raw_input("Enter you choice: ")

        if choice=="a":
            self_info()

        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)

        elif choice=="c":
           get_own_post()

        elif choice=="d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)

        elif choice=="e":
           insta_username = raw_input("Enter the username of the user: ")
           get_like_list(insta_username)

        elif choice=="f":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)

        elif choice=="g":
           insta_username = raw_input("Enter the username of the user: ")
           get_comment_list(insta_username)

        elif choice=="h":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)

        elif choice=="i":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)

        elif choice=="j":
            exit()

        else:
            print "wrong choice"

start_bot()
