This is a fork of abrenzel's python wrapper for the linkedin api: https://github.com/mrgaaron/LinkedIn-Client-Library/

His is very nice, but the search stuff is broken. Search should work here, although it's a bit hacky.
I've added support for field selector strings, too.
See the docs here:
    http://developer.linkedin.com/docs/DOC-1191#
    
Here's an example of how to use the search:

from liclient import LinkedInAPI
api = LinkedInAPI(API_KEY, SECRET_KEY)
params = {'first-name': 'John', 'last-name': 'Smith'}
field_selector_string = '(people:(id,first-name,last-name,headline,public-profile-url),num-results)'
results = api.search(ACCESS_TOKEN, params, field_selector_string)
# do stuff with results

Dependencies:
    lxml
    httplib2 (for OAuth)

Installable via:

        python setup.py install

To get started:

1.  First, of course, we need to instantiate the API object with our consumer key and secret:

     consumer_key = 'mykey'
     consumer_secret = 'mysecret'
     APIClient = LinkedInAPI(consumer_key, consumer_secret)

2.  The first step for a new user is to retrieve a request token.  This is done like so:

     request_token = APIClient.get_request_token()

3.  Then, we generate the URL to send the user to for authentication (I know the first line is a little ugly, I will probably simplify this soon):

     authorization_url = APIClient.base_url + APIClient.authorize_path
     url = "%s?oauth_token=%s" % (authorization_url, request_token['oauth_token'])

4.  Once the user has authenticated, you will need to collect the oauth_verifier returned by the LinkedIn server in the URL.  This can be done
     either by having the user type it in themselves or collecting the URL argument on the redirect from LinkedIn.  However you decided to get it,
     this is how you use it:

     access_token = APIClient.get_access_token(request_token, oauth_verifier)

That's it!  You can use this access token for every request this particular user makes, for as long as they have authorized you to use it.
