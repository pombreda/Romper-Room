# Romper Room

## Intro

Romper Room is a sample Django project that I use as a reference.  It shows a few handy things that you may want to use in your own projects.  The overall project layout is my standard layout strategy, which is described in detail in my [Django skeleton project](https://github.com/jordanorelli/Django-Skeleton).  For this project, I also included some sample [gunicorn](http://gunicorn.org/), [nginx](http://nginx.org/), and [supervisor](http://supervisord.org/) configurations.  These are minimal configurations for messing around; I wouldn't use these in a serious production environment.  [I also host a live demo of the projects at romper-room.jordanorelli.com](http://romper-room.jordanorelli.com/).

## OAuth

For both Facebook and Foursquare, I use a common authorization flow that is known by a variety of names, but which is called the ["authorization code grant" in the latest version of the OAuth spec](http://tools.ietf.org/html/draft-ietf-oauth-v2-23#section-4.1).  It is commonly called the "server flow".  Effectively the order of events is that your application redirects the user to Facebook/Foursquares auth server.  The auth server prompts them to log in, and upon logging in, redirects them back to our application.  When redirecting the user back to our application, the provider (Facebook/Foursquare) redirects the user to a url on our application that is known in advance.  A querystring is appended to the redirection url that contains a token that can be used by our server in exchange for hte user's OAuth token.  I use the very excellent [requests library](http://python-requests.org) to make the token request to the provider a bit cleaner.  The OAuth tokens are saved in our database for future use; there are models that correspond to the users Facebook/Foursquare profiles found in the `fb/models.py` and `dj4sq/models.py` files.  Once we have the user's OAuth token, we can use this to make calls to the Foursquare and Facebook APIs.

I do something that's a bit atypical in this project in that I use the server flow, but then I serve the page with the user's OAuth token in it.  With the OAuth token available on the client, I make ajax requests to the appropriate providers from the client, which saves the server some overhead.  This isn't necessarily the safest option since in the event of a [man-in-the-middle](http://en.wikipedia.org/wiki/Man-in-the-middle_attack) attack, an attacker could seize the user's OAuth credentials and pose as our application; if you're using this type of strategy, be sure to add ssl encryption to your application.  Since this is a sample application I didn't want to bother registering an SSL cert to do so.  It's also not at all compatible with IE at the moment because it runs into some problems with cross-origin resource sharing.  (If you know how to handle this and want to add support for it, it would be highly appreciated!)

## Hacking Django authentication backends

I added two sample backends, one for each of our OAuth providers.  This allows a user to sign in using only their OAuth token.  Right now I'm just randomly generating usernames and creating users on their first login.  By structuring it in this way, if a user connects both providers, we store both keys in a way that is related; we are able to determine which Facebook and Foursquare accounts are actually the same user.  Upon future visits, the user can authenticate with just one of the tokens, and since we've saved the OAuth tokens, we can continue to contact the other provider.

[(Django project documentation on authoring authentication backends)](https://docs.djangoproject.com/en/1.3/topics/auth/#writing-an-authentication-backend)

## Adding a {% raw %} tag to Django templates.

I added a `{% raw %}` tag to the Django template engine to allow me to embed [Mustache templates](http://mustache.github.com/) into the front end.  The Mustache templates themselves are used for rendering the Foursquare and Facebook API responses to the DOM.  There's a reference to the implementation [here](https://gist.github.com/629508), where it is referred to as the "verbatim" tag.  I just renamed it to raw.  nbd.  I honestly don't know why this isn't included in the Django templating language to begin with; it seems like an oversight.

## Embedding Mustache templates inside Django templates

I have no idea what the browser compatibility is for this, so I don't know that I'd go about using this strategy in a real-life application, but in this project I embedded Mustache templates into my Django template y adding `<script>` tags that are declared with the `text/plain` type so that the browser doesn't parse them as JavaScript, gave them an id, and used jQuery to select the tags and extract their contents.  It looks a lot cleaner to me than putting a big, ugly-ass string into your js.

## Conclusion

This is just a sample of how you can work with Django's pluggable auth system, and how it can be used to integrate with OAuth providers by hand.  I didn't use any canned OAuth, Foursquare, or Facebook libraries.  After doing this project, I'm not all that convinced they're entirely necessary for simple use cases.  The OAuth spec is already a fairly straightforward interface for dealing with external resource providers; at no point while writing this did I feel like I should just be using some canned library.  For more complex cases, where I'm using a lot of the resources availble through these APIs, I'd almost certainly use a wrapper, but for simple cases like this one, you'd be surprised how easy it is to just do it on your own.  Hope you find the project helpful!
