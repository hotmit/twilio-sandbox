# Features
* [ ] Send sms
* [ ] text-to-speech call
    * [ ] Get acknowledge response
* [ ] i18n speech

# Requirements
* Twilio >= 3.3.6

# Config
```
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