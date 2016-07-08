[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### GitHub Emailer: A Tool for Following Organizations

At some point GitHub had a way to follow organizations. They later decided that such a feature didn't make sense, because "organizations don't themselves do anything—users do." 

But I often care more about projects produced by agglomerations of people, so this is rather a pain.

This Python app/script:

1. Takes a list of GitHub organizations (as a Gist text file, with one organization per row);
2. Uses the [GitHub Search API](https://developer.github.com/v3/search/#search-repositories) to find any repositories they created over the past week; and
3. Sends these updates to you in an email "newsletter."

The whole thing is running on Heroku using the Scheduler add-on, with Sendgrid assisting with email delivery.

To reuse:

1. Click the deploy to Heroku button (or fork/clone)
2. Fill in all the environment variables you can
3. Get a Sendgrid API key with email sending permissions by clicking on the add-on and rifling through the settings
4. Set up Scheduler to run `python run.py` daily (there is no weekly option, though you can set the actual day you want to be emailed in the environment variables)

Next steps (maybe, maybe not)?

- Make email template prettier/more informative
- Store followed organizations in a fancier way
- Simplify follow/unfollow process
