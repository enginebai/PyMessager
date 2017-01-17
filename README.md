# PyMessager
PyMessager is a project to demostrate the simple bot development on [Facebook Message Platform](https://medium.com/r/?url=https%3A%2F%2Fdevelopers.facebook.com%2Fdocs%2Fmessenger-platform) using Python Flask and provide Python API to help you develop your bot on Facebook.

![Our startup](https://raw.githubusercontent.com/enginebai/PyMessager/master/art/dualcores.png)

A full tutorial to on [My Medium](https://medium.com/@enginebai/用python開發facebook-bot-26594f13f9f7#.7iwm148ag) and you can find more detail information to setup before coding and get starting the project.

## Before Coding
1. Prepare a facebook pages. (to create if you don't have one)
2. Start a developer application at [facebook to developer](https://developers.facebook.com).
3. Create a python project, and install the required packages and modules: [Flask](http://flask.pocoo.org), [Requests](http://docs.python-requests.org/en/master/).
4. Use [Let's Encrypt](https://letsencrypt.org/getting-started/) to apply SSL cerificiation for your domain name.

## Getting Started
There are three main steps:

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
There are serveral types of message: text, image, button template or generic templates. API provides different enumerations and classes to generate the message template.

All you have to do is clone this project and import source code to your project. 

> Next time I will make a setup module so that you can install via `pip`.


### Import
```python
from message import SendMessage
```

### Text
![](https://raw.githubusercontent.com/enginebai/PyMessager/master/art/text.png)

```python
SendMessage(recipient_id)
	.build_text_message("嗨，我是昌永，DualCores Studio共同創辦人和Developer")
	.send_message()
```

### Image
![](https://raw.githubusercontent.com/enginebai/PyMessager/master/art/image.png)

```python
SendMessage(recipient_id)
	.build_image_message("http://image-url.jpg")
	.send_message()
```

### Button Template
![](https://raw.githubusercontent.com/enginebai/PyMessager/master/art/button.png)

```python
SendMessage(sender).build_buttons_message("直接訂位或查看官方網站？", [
	ActionButton(ButtonType.POSTBACK, 
					'直接訂位', 
					payload=Payload.RESERVATION),
	ActionButton(ButtonType.WEB_URL, 
					'官方網站', 
					url="https://dual-cores.com")])
```
### Generic Template
![](https://raw.githubusercontent.com/enginebai/PyMessager/master/art/generic.png)

```python
message = SendMessage(recipient_id)
project_styletrip = GenericElement('Styletrip時代遊',
                                   '一站式的自動旅遊排程',
                                   HOST + PROJECT_DIR + 'styletrip/introduction.jpeg', [
                                       ActionButton(ButtonType.POSTBACK,
                                                    '詳細介紹',
                                                    payload=Payload.INTRODUCE.name)
                                   ])
project_movie_lol = GenericElement('Movie lol App',
                                   '電影資訊和評價App',
                                   HOST + PROJECT_DIR + 'movielol/introduction.jpeg', [
                                       ActionButton(ButtonType.WEB_URL,
                                                    'GitHub連結',
                                                    url='https://github.com/enginebai/Movie-lol-android')
                                   ])
message.build_generic_message([project_styletrip, project_movie_lol]).send_message()
```

## API
### SendMessage(recipient_id)
The class represents the message entity object which sent to the user. Provide the `recipient_id` which must be an id that was retrieved throught the Facebook message API and choose one message and fill the content. 

#### `build_text_message(title_text)`
* `title_text`: The message content.

#### `build_image_message(image_url)`
* `image_url`: The image url show in message.

#### `build_buttons_message(title_text, button_list)`
* `title_text`: The message content.
* `button_list`: The list of `ActionButton`.

#### `build_generic_message(element_list)`
* `element_list`: The list of `GenericElement` objects.

#### `send_message()`
* **Make sure call this API after building a message.**

### ButtonType
The enum provide two value to specify the type of button.

* `WEB_URL`: Provide a link opened by browser.
* `POSTBACK`: Provide a call-to-action id, which is used to identify the data sent back to your server via webhook. 


### ActionButton(button_type, title, url=None, payload=None)
The class defines the call-to-action button object used in Button Template.

* `button_type`: The type of button, value is `ButtonType.WEB_URL` or `ButtonType.POSTBACK`.
* `title`: The message content.
* `url`: the url opened in browser, required if `button_type == ButtonType.WEB_URL`.
* `payload`: the postback id, required if `button_type == ButtonType.POSTBACK`.


### GenericElement(title, subtitle, image_url, buttons)
The class defines one of bubble in one message.

* `title_text`: The message main title.
* `subtitle_text`: The message subtitle, leave empty string if no subtitle in your message.
* `button_list`: The list of `ActionButton`


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

