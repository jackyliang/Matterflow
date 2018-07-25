# Matterflow

Welcome to Matterflow, a Stack Overflow integration built into Mattermost!

![matterflow_demo](https://user-images.githubusercontent.com/4315746/43174571-accb2722-8f6f-11e8-813a-fb0da88b5db7.gif)

## How do I use Matterflow?

We currently offer the following functionality, with more to come:

- [/search](http://api.stackexchange.com/docs/answers-on-questions) `<search query>` - Get all the results for a certain search query
- [/question](http://api.stackexchange.com/docs/answers-by-ids) `<question ID>` - Get all the answers for a specific question ID (which can be retrieved by `/search`)
- [/ask](https://stackoverflow.com/questions/ask) - Gets a link for you to ask a question on Stack Overflow
- /help - For when you get lost. It's okay, we're all a little lost sometimes :)
- and more to come!

## How can I install Matterflow in my Mattermost channel?

1. Go to your **Channel**
2. Navigate to the **Main Menu** dropdown
3. Click **Integrations**
4. Once you're in the Integrations page, click **Slash Command** and then **Add Slash Command**
4. Fill in the following information:
- Title: `Matterflow`
- Description: `Stack Overflow for Mattermost`
- Command Trigger Word: `so`
- Request URL: `https://matterflow.herokuapp.com/so`
- Request Method: `POST`
- Response Username: `Matterflow`
- Autocomplete: :white_check_mark:
- Autocomplete Hint: `'help' for all available commands!`
- Autocomplete Description: `Stack Overflow for Mattermost`

## How do I further develop this integration?

Clone it to your machine

    $ git clone git@github.com:jackyliang/Matterflow.git matterflow

Navigate to the directory

    $ cd matterflow

Install local required files for the application

    $ pip install -r requirements.txt

Start the application! (That was easy)

    $ python app.py

You can also query the local application to test each endpoint

    $ curl -XPOST -d 'text=search python array' 'http://0.0.0.0:5000/so'
    $ curl -XPOST -d 'text=help' 'http://0.0.0.0:5000/so'


## How do I deploy this integration?

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

**Important**: Make sure you have your StackExchange key entered under **Settings** -> **Config Var** within Heroku

![](https://user-images.githubusercontent.com/4315746/43174113-379e9238-8f6d-11e8-8b4b-9a046937e223.png)

This gives you additional requests for querying Stack Exchange. This is necessary if your channel or organization uses this feature a lot.

**Pro tip:** You can enable Heroku auto-deployment by connecting it to the Github repo. Everytime you push to the repo, Heroku will deploy automatically.

![](https://user-images.githubusercontent.com/4315746/43174172-73d0e4e0-8f6d-11e8-896c-f1f04acfc0c5.png)

## I need help debugging..

When developing a new command, you may run into issues with querying the API either in Heroku or Mattermost. To debug these API issues, I highly recommend using Heroku's **View logs** feature under:

![](https://user-images.githubusercontent.com/4315746/43174316-3e04f058-8f6e-11e8-95ef-707cd50a538e.png)

Additionally, you can also debug Mattermost request issues through the **System Console** -> **Logging**

![](https://user-images.githubusercontent.com/4315746/43174358-7bca18e6-8f6e-11e8-9ffa-157dfe2a474b.png)

## How can I contribute?

Feel free to file bugs and makes suggestions with [Github Issues](https://github.com/jackyliang/Matterflow/issues)!

Want to give feedback or thank the creator? You can find him on Twitter at [@jjackyliang](https://twitter.com/jjackyliang)