# PyMessager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PyMessager is a [Facebook Messager](https://developers.facebook.com/docs/messenger-platform) Python SDK and a sample project to demostrate how to develop a bot on Facebook Messager.

![](https://raw.githubusercontent.com/enginebai/PyMessager/master/art/graphic.png)

A full tutorials are on [Develop Facebook bot using python](https://medium.com/@enginebai/用python開發facebook-bot-26594f13f9f7#.7iwm148ag) and [Chatbot: from 0 to 1]() where you can find more detail information to setup and develop.

## Setup
1. Prepare a facebook pages. (to create if you don't have one)
2. Start a developer application at [facebook to developer](https://developers.facebook.com).
3. Create a python project, and install the required packages and modules: [Flask](http://flask.pocoo.org), [Requests](http://docs.python-requests.org/en/master/).
4. Use [Let's Encrypt](https://letsencrypt.org/getting-started/) to apply SSL cerificiation for your domain name.

## Install
To install pymessager, simply run:

```shell
$ pip install pymessager
```

or install from repository:

```shell
$ git clone git@github.com:enginebai/PyMessager.git
$ cd PyMessager
$ pip install -r requirements.txt
```

## 
There are three main steps to prepare for you bot:

1.Setup the Webhook.

```python
@app.route(API_ROOT + FB_WEBHOOK, methods=["GET"])
def fb_webhook():
    verification_code = 'I_AM_VERIFICIATION_CODE'
    verify_token = request.args.get('hub.verify_token')
    if verification_code == verify_token:
        return request.args.get('hub.challenge')
```        

2.Receive the message.

```python
@app.route(API_ROOT + FB_WEBHOOK, methods=['POST'])
def fb_receive_message():
    message_entries = json.loads(request.data.decode('utf8'))['entry']
    for entry in message_entries:
        messagings = entry['messaging']
        for message in messagings:
            sender = message['sender']['id']
            if message.get('message'):
                text = message['message']['text']
                print("{} says {}".format(sender, text))
    return "Hi"
```

3.Start the server with https.

```python
if __name__ == '__main__':
    context = ('ssl/fullchain.pem', 'ssl/privkey.pem')
    app.run(host='0.0.0.0', debug=True, ssl_context=context)
```


## Usage

![](https://raw.githubusercontent.com/enginebai/PyMessager/master/art/usage.png)

There are serveral types of message: `text`, `image`, `button template` or `generic template`. API provides different enumerations and classes to generate the message template.


### Import
```python
from message import Messager, QuickReply, GenericElement, ActionButton, ButtonType
```

### Initialization
You can initialize the messager client via providing the facebook access token from developer console:

```python
from message import Messager
client = Messager(config.facebook_access_token)
```

### Subscribe the pages
Before your chatbot starts to receive the message, you have to subscribe the application to your chatbot page. To subscribe a page, just call it:

```python
client.subscribe_to_page()
```

### Set the welcome message and get-started button
![](https://raw.githubusercontent.com/enginebai/PyMessager/master/art/onboarding.png)

The greeting text will show at the first time you open this chatbot on mobile only. The payload is the trigger when the users click "Get Started" button.

```python
client.set_greeting_text("Hi, this is Engine Bai. Nice to meet you!")
client.set_get_started_button_payload("HELP")  # Specify a payload string.
```

### Sending a text and image
* Make sure that image URL is a valid link.

```python
client.send_text(recipient_id, "Hello, I'm enginebai."
client.send_image(recipient_id, "http://image-url.jpg")
```

### Quick Replies
```python
client.send_quick_replies(self.sender, "Help", [
         QuickReply("Projects", Intent.PROJECT),
         QuickReply("Blog", Intent.BLOG),
         QuickReply("Contact Me", Intent.CONTACT_ME
     ])
```

### Button Template


```python
client.send_buttons(recipient_id, "你可以透過下列方式找到我", [
    ActionButton(ButtonType.WEB_URL, "Blog", "http://blog.enginebai.com"),
	ActionButton(ButtonType.POSTBACK, "Email", Intent.EMAIL)
])
```
### Generic Template
The `GenericElement` class defines one of bubble in one message.

* `title_text`: The message main title.
* `subtitle_text`: The message subtitle, leave empty string if no subtitle in your message.
* `button_list`: The list of `ActionButton`

```python
project_list = []
for project_id in projects.keys():
    project = projects[project_id]
    project_list.append(GenericElement(
        project["title"],
        project["description"],
        config.api_root + project["image_url"], [
            ActionButton(ButtonType.POSTBACK,
                         self._get_string("button_more"),
                         # Payload用Intent本身作為開頭
                         payload=Intent.PROJECTS.name + project_id)
        ]))
self._messager.send_generic(recipient_id, project_list)
```

## Issues
Feel free to submit bug reports or feature requests and make sure you read the contribution guideline before opening any issue.


## Contributing
1. Check the open/close issues or open a fresh issue for feature request or bug report with different labels (`feature`/`bug`).
2. Fork this [repository](https://github.com/enginebai/PyMessager) on GitHub to start customizing on master or new branch.
3. Write a test which shows that the feature works as expected or the bug was fixeed.
4. Send a pull request and wait for code review.

[Read more on contributing](./CONTRIBUTING.md).

## License

	The MIT License (MIT)

	Copyright © 2016 Engine Bai.

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	THE SOFTWARE.

