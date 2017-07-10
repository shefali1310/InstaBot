#Importing requests and urlib packages.
import requests , urllib

#Importing termcolor
from termcolor import colored

import re
#Importing textblob - to analyze the sentiments of the comments.
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#importing wordcloud library - to generate a wordcloud of user's interests.
from wordcloud import WordCloud, STOPWORDS

#importing matplot library - to plot the interests
import matplotlib.pyplot as plt



#This is the access token for accessing the instagram API
APP_ACCESS_TOKEN = '286308105.a90ec70.7691dca881004b60b57db1cc85505c1e'

#Token owner = shefaliyadv
#Sandbox users = insta.bot.test.0, insta.bot.test.1, instabotmriutest0

#This is the base URL for the instagram API.
BASE_URL = 'https://api.instagram.com/v1/'






#Working
# 1. Function that retrives the value of your own instagram account - followers, list of following, number of posts, etc.

def my_info():
  request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()


  if user_info['meta']['code'] == 200:

      if len(user_info['data']):
          print colored('Username: %s','blue') % (user_info['data']['username'])
          print colored('No. of followers: %s','blue') % (user_info['data']['counts']['followed_by'])
          print colored('No. of people you are following: %s','blue') % (user_info['data']['counts']['follows'])
          print colored('No. of posts: %s','blue') % (user_info['data']['counts']['media'])
      else:
          print colored('User does not exist!','red')

  else:
      print colored('Status code other than 200 received!','red')





#Working
# Function declaration to get the id of the user.

def fetch_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None

    else:
        print colored('Status code other than 200 received!','red')
        exit()






# 2. Function declaration to get the info of a user by username

def fetch_user_info(insta_username):
    user_id = fetch_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)

    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if len(user_info['data']):
            print colored('Username: %s','blue') % (user_info['data']['username'])
            print colored('No. of followers: %s','blue') % (user_info['data']['counts']['followed_by'])
            print colored('No. of people you are following: %s','blue') % (user_info['data']['counts']['follows'])
            print colored('No. of posts: %s','blue') % (user_info['data']['counts']['media'])
        else:
            print colored('There is no data for this user!','red')

    else:
        print colored('Status code other than 200 received!','red')






# 3. Function declaration to get any post of your own account.(range 0-19)

def fetch_your_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:

        if len(own_media['data']):

            own_post_number = int(raw_input("Enter the image number you would like to download."))
            image_name = own_media['data'][own_post_number]['id'] + '.jpeg'
            image_url = own_media['data'][own_post_number]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded!','green')
        else:
            print colored('Post does not exist!','red')

    else:
        print colored('Status code other than 200 received!','red')






# 4. Function declaration to get the any post of another user(Index range from 0-19)


def fetch_user_post(insta_username):
    user_id = fetch_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!','red')
        exit()

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:

        if len(user_media['data']):

            post_number = int(raw_input("Enter the post number you would like to download")) #Please Note: if entered '20', index out of range error is shown.
            image_name = user_media['data'][post_number]['id'] + '.jpeg'
            image_url = user_media['data'][post_number]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)

            print colored('Your image has been downloaded!','green')
        else:
            print colored('Post does not exist!','red')

    else:
        print colored('Status code other than 200 received!','red')



# Function to retrieve own post id

def fetch_own_post_id():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            return own_media['data'][0]['id']
        else:
            print colored('Post does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')






#Function declaration to get the post id of another user's recent post.

def get_post_id(insta_username):
    user_id = fetch_user_id(insta_username)
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
            print colored('There is no recent post of the user!','red')
            exit()

    else:
        print colored('Status code other than 200 received!','red')
        exit()







# Working
# 5. Function declaration to get a list of the likers for a particular post.

def fetch_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token= %s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    list_of_likes_info = requests.get(request_url).json()

    if list_of_likes_info['meta']['code'] == 200:

        if len(list_of_likes_info['data']):
            for x in range(len(list_of_likes_info['data'])):
                print 'list of likes is %s' % (list_of_likes_info['data'][x]['username'])
        else:
            print colored('likes does not exist.', 'red')

    else:
        print colored('status code other than 200 received.', 'red')







#Working
# 6. Function declarartion to post a like on the user's media.

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like['meta']['code'] == 200:
        print colored('Like was successful!','green')
    else:
        print colored('Your like was unsuccessful. Please try again!','red')

# Working
# 7. Function declaration to get the comment list from the user's post.

def get_comments_list(insta_username):
    media_id = get_post_id(insta_username)
    if media_id is None:
        print colored("There is no media", 'red')
    else:
        request_url = BASE_URL + "media/%s/comments/?access_token=%s" % (media_id, APP_ACCESS_TOKEN)
        print "Get request url:%s" % request_url
        comment_list = requests.get(request_url).json()

    # check the status code, if comes 200 then show the list of comments
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            print "The comments on the post :"
            for x in range(len(comment_list['data'])):
                comment_text = comment_list['data'][x]['text']
                print "comment: %s" % (comment_text)

        else:
            print colored("No comments on this post", 'red')
    else:
        print colored("Status code other than 200", 'red')


#Working
# 8. Function declaration to post a comment on a user's media

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)
    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print colored('Successfully added a new comment!','green')
    else:
        print colored('Unable to add comment. Please try again!','red')







#Working
# 9. Function declaration to delete negative comments from a user's post.

def delete_negative_comments(insta_username):
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  comment_info = requests.get(request_url).json()

  if comment_info['meta']['code'] == 200:

    if len(comment_info['data']):

        for x in range(len(comment_info['data'])):
            comment_id = comment_info['data'][x]['id']
            comment_text = comment_info['data'][x]['text']
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

            if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                print 'Negative comment : %s' % (comment_text)
                delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                media_id, comment_id, APP_ACCESS_TOKEN)

                print 'DELETE request url : %s' % (delete_url)
                delete_info = requests.delete(delete_url).json()

                if delete_info['meta']['code'] == 200:
                    print colored('Comment successfully deleted!\n','green')
                else:
                    print colored('Unable to delete comment!','red')

            else:
                print colored('Positive comment: %s\n','red') % (comment_info)

    else:
        print colored('There are no comments on this post.','red')

  else:
      print colored('Status code other than 200 received!','red')








#Working.
# 11. Function to get information of your own comment

def own_comment_info():
    media_id = fetch_own_post_id()
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info):
            x = 0
            for x in range(len(comment_info["data"])):
                print "%s commented : %s" % (["data"][x]["from"]["username"],["data"][x]["text"])
                x = x + 1

        else:
            print colored("No comments have been made.",'red')
    else:
        print colored("Status codde other than 200 received.",'red')






# Function to get the list of hashtags of all the posts of a user.

def hashtag_analysis(insta_username):

    # Defining a list where the hashtags of the user will be stored.
    Hashtag_list = []

    user_id = fetch_user_id(insta_username)
    if user_id == None:
        print colored("No user found.",'red')

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'Get request url: %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code']== 200:
        if len(user_media):
            for x in range(len(user_media['data'])):
                hashtags = user_media['data'][x]['tags']
                print hashtags
                Hashtag_list.append(hashtags)
                str1 = str(Hashtag_list)


                generate_wordcloud(str1)




        else:
            print colored("Media doesn't exist",'red')
    else:
        print colored("Status code other than 200 received.",'red')


def generate_wordcloud(str1):

    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='black',
                          width=1200, height=1000).generate(str1)

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('wordcloud.png')
    plt.show()





#Function declarartion to run the bot.

def start_bot():

    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "1.Get your own details\n"
        print "2.Get details of a user by username\n"
        print "3.Get your own recent post\n"
        print "4.Get the recent post of a user by username\n"
        print "5.Get a list of people who have liked the recent post of a user\n"
        print "6.Like the recent post of a user\n"
        print "7.Get a list of comments on the recent post of a user\n"
        print "8.Make a comment on the recent post of a user\n"
        print "9.Delete negative comments from the recent post of a user\n"
        print "10.Plot your friend's interests.\n"
        print "11.Get your own commednt info.\n"
        print "12.Exit the instabot.\n"

        choice=raw_input("Enter you choice: ")

        # Nested Loop starts here.

        if choice == "1" :
            my_info()

        elif choice == "2" :
            insta_username = raw_input("Enter the username of the user: ")
            fetch_user_info(insta_username)

        elif choice == "3" :
           fetch_your_own_post()

        elif choice == "4" :
            insta_username = raw_input("Enter the username of the user: ")
            fetch_user_post(insta_username)

        elif choice == "5":
           insta_username = raw_input("Enter the username of the user: ")
           fetch_like_list(insta_username)

        elif choice == "6" :
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)

        elif choice == "7" :
           insta_username = raw_input("Enter the username of the user: ")
           get_comments_list(insta_username)

        elif choice == "8" :
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)

        elif choice == "9" :
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comments(insta_username)

        elif choice == "10" :
            insta_username = raw_input("Enter the name of the user:")
            hashtag_analysis(insta_username)

        elif choice == '11':
            own_comment_info()

        elif choice == "12" :

            exit()

        else:
            print colored("wrong choice",'red')

start_bot()
