Standard stuff applies to install.  Run this from
the command line:

        python setup.py install
        
Documentation is in the doc directory.  Any questions
can be forwarded to abrenzel@millerresource.com.  I'm
usually pretty good about responding.

The LinkedIn client library has lxml as a dependency for
XML processing.  Yes, I know Python has a standard XML
parser implementation.  Yes, I know lxml can be a bear to install
if you're building from source.  Still, there's no faster or
more full-featured XML parsing tool available for Python.  I 
have no plans to include support for the etree parser in the
standard libary.

One other dependency is httplib2 (for the OAuth module).  You
can obtain this module from the Python Package Index.

This package is intended for use with the LinkedIn API.  
You must supply your own API key for this library to work.
Once you have an API key from LinkedIn, the syntax for instantiating
an API client object is this:

	mykey = 'mysecretkey'
	mysecret = 'mysecretsecret'
	myclient = LinkedInAPI(mykey, mysecret)

From there, you can obtain request tokens, authorization urls,
access tokens, and actual LinkedIn data through the LinkedInAPI
object's methods.  The object will handle signing requests, url
formatting, and XML parsing for you.  Full documentation for these
methods can be found in the doc directory (or will be there when 
I get it done).

Happy apping!

Aaron
