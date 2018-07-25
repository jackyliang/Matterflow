# Matterflow

Welcome to Matterflow, a Stack Overflow integration built into Mattermost!

### How do I use Matterflow?

We currently offer the following functionality, with more to come.

This integration offers functionality such as:
- [/search](http://api.stackexchange.com/docs/answers-on-questions) `<search query>` - Get all the results for a certain search query
- [/question](http://api.stackexchange.com/docs/answers-by-ids) `<question ID>` - Get all the answers for a specific question ID (which can be retrieved by `/search`)
- [/ask](https://stackoverflow.com/questions/ask) - Gets a link for you to ask a question on Stack Overflow
- and more to come!

### How can I install Matterflow in my Mattermost channel?

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
- Autocomplete Hint: `help` for all available commands!
- Autocomplete Description: Stack Overflow for Mattermost

### How do I further develop this integration?

Install local required files for the application

    $ pip install -r requirements.txt

Start the application

    $ python app.py


Query the local application

    $ curl -XPOST -d 'text=search python array' 'http://0.0.0.0:5000/so'
    $ curl -XPOST -d 'text=help' 'http://0.0.0.0:5000/so'


### How do I deploy this integration?

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

**Important**: Make sure you have your StackExchange key entered under **Settings** -> **Config Var** within Heroku

![](https://imgur.com/EEh1Rze)

This gives you additional requests for querying Stack Exchange. This is necessary if your channel or organization uses this feature a lot.


### How can I contribute?

Feel free to file bugs and makes suggestions with [Github Issues](https://github.com/jackyliang/Matterflow/issues)!

Want to give feedback or thank the creator? You can find him on Twitter at [@jjackyliang](https://twitter.com/jjackyliang)