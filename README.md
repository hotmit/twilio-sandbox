# Features
* [ ] Send sms
* [ ] text-to-speech call
    * [ ] Get acknowledge response
* [ ] i18n speech

# Requirements
* Twilio >= 3.3.6

# Config
```python
# BASE_DIR/twilio_config.py
twilio_config = {
    'account': '',
    'token': '',
    'phone_number': 'from_ number',         
}

twilio_test = {
    'default_phone_no': 'pre-filled number for test',
}
```

# Twilio API
```python
# if you want gather to interrupt ur say, you can nested say with in the gather command
r = twiml.Response()
with r.gather(action=gather_url, timeout=10, numDigits=1) as g:    
    g.say(message, language=lang, voice=voice)
    
?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather action="/process_gather.php" method="GET">
        <Say>Enter something, or not</Say>
    </Gather>
</Response>
```