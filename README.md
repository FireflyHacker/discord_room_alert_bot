# room_alert_bot
Discord bot to alert people in the IEEE UCI Discord when the room is open

### Usage
Flip switch "On" to send a discord message alerting people the room is open. Flip switch "Off" to send a message alerting people that the room is closed. 

### Installation & Configuration
* Extract & Install on pi. Install `requests` library through pip.
* You need to rename `creds_CHANGEME.py` to `_creds_.py` and add your discord webhook to the `WEBHOOK_URL` field in the file. 

### General Info
* Program logs are located at `/var/log/ieee_room_alert/`. Permissions for this directory should be set with GID mask, and you should be running the program as a daemon using a user created just for it. 

### Indicator Light Behavior
* When operating correctly, only one light should be on at a time. The lights will ONLY change once a message has successfully been posted to discord.
* Blinking:
    * There should be a double blink on startup to indicate that the program has begun execution. 
    * On errors, they blink. If there's a lost network connection, or discord's servers are down, or anything else has caused several errors to rack up, the lights should alert the user that something's not right. 


### TODO:
* [ ] verify connection error handling works correctly
* [ ] implement logging
    * [ ] implement log rotation & sending via email
