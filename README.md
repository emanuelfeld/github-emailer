At some point GitHub had a way to follow organizations. They later decided that such a feature didn't make sense, because "organizations don't themselves do anything—users do." 

But I often care more about projects produced by agglomerations of people, so this is rather a pain.

This Python app/script:

1. Takes a list of GitHub organizations;
2. Uses the [GitHub Search API](https://developer.github.com/v3/search/#search-repositories) to find any repositories they created over the past week; and
3. Sends these updates to you in an email "newsletter."

Currently, I've put the organization list in a Gist text file (one organization name per row).

The whole thing is running on Heroku using the Scheduler add-on.

Next steps (definitely)

- Fill out app.json to make one-click deployable

Next steps (maybe)?

- Make email prettier/easier to parse
- Store followed organizations in a fancier way
- Simplify follow/unfollow process