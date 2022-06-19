from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from pathlib import Path
from dotenv import load_dotenv
import re
from slack_bolt.async_app import AsyncApp
import _asyncio
from datetime import date
from datetime import time
from datetime import datetime, timedelta
import time

# Get Todays Date
todayRaw = date.today()
today = todayRaw.strftime("%d/%m/%Y")
todayString = todayRaw.strftime("%B %d, %Y")

# Get Time and Date
timeCurrent = datetime.now()
dt_string = timeCurrent.strftime("%H:%M:%S on %B %d, %Y")

env_path = Path('.', '.env')

load_dotenv()
SLACK_BOT_TOKEN = "xoxb-3595728670692-3579097000695-S2Mds9XgpRee3YvSVN4nZamE"
SLACK_APP_TOKEN = "xapp-1-A03HFASR2E6-3670204359010-10538b51c718124b895e9f0c33ecfec75794b58a877e97535225b7feb285676c"
SLACK_SIGNING_SECRET = "849867a0e583a18f8ab8477e2d241e26"

app = App(token=SLACK_BOT_TOKEN)

#----------------------------------------------------------------------------------------------------------------------------------------------#

# Test Command for Programming Purposes
@app.command("/test")
def test(ack, respond, command):
    global SHIFT_NOTIFS, WORK_NOTIFS, FUN_NOTIFS, break_time, break_post, clockin_time, result
    ack()
    respond(str(result))

#----------------------------------------------------------------------------------------------------------------------------------------------#

# App Home Page
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:


    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
            {
                "type": "section",
                "text": {
                "type": "mrkdwn",
                "text": "*Welcome to Terry Timebot!* :tada:"
                }
            },
            {
                "type": "divider"
                },
            {
                "type": "section",
                "text": {
                "type": "mrkdwn",
                "text": "Hello! I'm here to help you with all your workshift needs - clocking in and out, requesting time off, and helping you take productive breaks."
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Developers Website"
                            }
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Here's what I can help you with:"
                    }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*1️⃣ Use the `/clockin` command*. Type `/clockin` or `/in` to easily clock in to work immediately!"
                    }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*2️⃣ Use the `/clockout` command*. Type `/clockout` or `/out` to clock out of your shift, just as easy as clocking in!"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Use the `/notifications` command*. Type `/notifications` or `/notifs` to configure your notification settings for during your shifts. I know you might not want to have me chatting while you're busy!"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "➕ If you need to schedule some time to relax, use the _Make a Leave Request_ action. This will be automatically submitted to your employer through me."
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "If you want to check your current timesheets but don't want to leave the comfort of Slack, use the _See Timesheets_ action. This will show your current shift summaries!"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "❓Get help at any time with `/help`"
                    }
                ]
            }
        ]
    }
)
  
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

#----------------------------------------------------------------------------------------------------------------------------------------------#

# When someone mentions the app
@app.event("app_mention")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
def mention_handler(body, say):
        say("Hello! Hope you're having a great day!");

# Someone says hello
@app.message(re.compile("(hi|Hi|hello|Hello|Hey|hey|:wave:)"))
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>! How's it going?");

@app.message(re.compile("(Tell me a joke|Tell a joke|Say a joke)"))
def tell_joke(message, say):
    user = message['user']
    say(f"I'm no clown, <@{user}>!");

#----------------------------------------------------------------------------------------------------------------------------------------------#

# Someone Joins
@app.event("team_join")
def ask_for_introduction(event, say):
    welcome_channel_id = "C03HCCVKH8D"
    user_id = event["user"]
    text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel. Feel free to message me if you need anything! use the /help command to learn more about how I can help you."
    say(text=text, channel=welcome_channel_id)

#----------------------------------------------------------------------------------------------------------------------------------------------#

# Help Command
@app.command("/help")
def help(ack, respond, command):
    # Acknowledge command request
    ack()
    respond({
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Hey there 👋 I'm Terry Timebot! I see you're wondering what I can do for you.\nHere's what I can help you with:"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*1️⃣ Use the `/clockin` command*. Type `/clockin` or `/in` to easily clock in to work immediately!"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*2️⃣ Use the `/clockout` command*. Type `/clockout` or `/out` to clock out of your shift, just as easy as clocking in!"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Use the `/notifications` command*. Type `/notifications` or `/notifs` to configure your notification settings for during your shifts. I know you might not want to have me chatting while you're busy!"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "➕ If you need to schedule some time to relax, use the _Make a Leave Request_ action. This will be automatically submitted to your employer through me."
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "If you want to check your current timesheets but don't want to leave the comfort of Slack, use the _See Timesheets_ action. This will show your current shift summaries!"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "❓Get help at any time with `/help`, or check out my homepage any time!"
                            }
                        ]
                    }
                ]
            }
        )

#----------------------------------------------------------------------------------------------------------------------------------------------#

# Whether they've clocked in or not
CLOCKIN_STATUS = 0

# Track clock in and out time
clockin_time = datetime.now()
clockout_time = timeCurrent

# Track length of last shift
LAST_SHIFT_LENGTH = 0
hours = 0
mins = 0

break_time = 0
break_post = 0

result = 0

# Clocking In
@app.command("/clockin")
def clock_in(ack, respond, client, command, logger):
    global CLOCKIN_STATUS, clockin_time, SHIFT_NOTIFS, break_time, break_post
    # Acknowledge command request
    ack()
    if CLOCKIN_STATUS == 0:
        timeCurrent = datetime.now()
        clockin_time = timeCurrent
        respond("You are clocking in at " + clockin_time.strftime("%I:%M %p on %B %d, %Y") + "! Enjoy your work day!")
        
        CLOCKIN_STATUS = 1
        if SHIFT_NOTIFS == 1:
            # One Minute Break Message
            try:
                break_time = clockin_time + timedelta(seconds=60)
                break_post = time.mktime(break_time.timetuple())
                short_break = client.chat_scheduleMessage(
                    channel="C03L803R76W",
                    text="Hello there! Here's a one minute break reminder, to demonstrate how this notification would go through! Feel free to take a break now, you deserve it! :D",
                    post_at=time.mktime(break_time.timetuple())
                )
                logger.info(short_break)
            except Exception as e:
                # Handle error
                logger.exception(f"Failed to post a message {e}")
            # 4 Hour Break Message
            try:
                break_time = clockin_time + timedelta(hours=4)
                break_post = time.mktime(break_time.timetuple())
                short_break = client.chat_scheduleMessage(
                    channel="C03L803R76W",
                    text="You've been working for 4 hours! Time for a short break, at least! If you're working longer than 5 hours today, you can consider taking your 30 minute lunch break if you feel like it.",
                    post_at=time.mktime(break_time.timetuple())
                )
                logger.info(short_break)
            except Exception as e:
                # Handle error
                logger.exception(f"Failed to post a message {e}")

            # 5 Hour Break Message
            try:
                break_time = clockin_time + timedelta(hours=5)
                break_post = time.mktime(break_time.timetuple())
                short_break = client.chat_scheduleMessage(
                    channel="C03L803R76W",
                    text="It's been 5 hours, wow! If you haven't taken a break yet, you should definitely take at least a 10 minute one now. If you haven't had your lunch break yet, you're good to go!",
                    post_at=time.mktime(break_time.timetuple())
                )
                logger.info(short_break)
            except Exception as e:
                # Handle error
                logger.exception(f"Failed to post a message {e}")

            # 7 Hour Break Message
            try:
                break_time = clockin_time + timedelta(hours=7)
                break_post = time.mktime(break_time.timetuple())
                short_break = client.chat_scheduleMessage(
                    channel="C03L803R76W",
                    text="7 hours today, nice job! If you haven't taken your 30 minute break, you definitely should, you've earned it! Otherwise, if you're feeling a bit tired, you're free to take your second 10 minute break any time.",
                    post_at=time.mktime(break_time.timetuple())
                )
                logger.info(short_break)
            except Exception as e:
                # Handle error
                logger.exception(f"Failed to post a message {e}")

            # 8 Hour Break Message
            try:
                break_time = clockin_time + timedelta(hours=8)
                break_post = time.mktime(break_time.timetuple())
                short_break = client.chat_scheduleMessage(
                    channel="C03L803R76W",
                    text="8 hours, good going! If you haven't taken a second 10 minute break yet, now is a great time to relax and reset for the final stretch.",
                    post_at=time.mktime(break_time.timetuple())
                )
                logger.info(short_break)
            except Exception as e:
                # Handle error
                logger.exception(f"Failed to post a message {e}")

            # 10 Hour Break Message
            try:
                break_time = clockin_time + timedelta(hours=10)
                break_post = time.mktime(break_time.timetuple())
                short_break = client.chat_scheduleMessage(
                    channel="C03L803R76W",
                    text="10 hours!?! You're doing amazing! If you'd like your second 30 minute break, you've definitely earned it!",
                    post_at=time.mktime(break_time.timetuple())
                )
                logger.info(short_break)
            except Exception as e:
                # Handle error
                logger.exception(f"Failed to post a message {e}")

        return
    if CLOCKIN_STATUS == 1:
        respond("You have already clocked in today at " + clockin_time.strftime("%I:%M %p on %B %d, %Y") + ". Would you like to clock out? Just use `/clockout` instead!")
        return

# Clocking Out
@app.command("/clockout")
def clock_out(ack, respond, client, command, logger):
    # Acknowledge command request
    global CLOCKIN_STATUS, result
    ack()
    if CLOCKIN_STATUS == 1:
        timeCurrent = datetime.now()
        clockout_time = timeCurrent
        shift_time = clockout_time - clockin_time
        minutes = divmod(shift_time.seconds, 60)
        hrs_mins = divmod(minutes[0], 60)
        hours = hrs_mins[0]
        mins = hrs_mins[1]
        LAST_SHIFT_LENGTH = hrs_mins
        respond("You are clocking out at " + timeCurrent.strftime("%I:%M %p on %B %d, %Y") + ". Your shift time was " + str(hours) + " hours, " + str(mins) + " minutes. See you next time!")
        CLOCKIN_STATUS = 0
        result = client.chat_scheduledMessages_list(
        )
        channel_id_list = []
        message_id_list = []

        for message in range(len(result['scheduled_messages'])):
            channel=result['scheduled_messages'][message]['channel_id']
            scheduled_message_id=result['scheduled_messages'][message]['id']
            channel_id_list.append(channel)
            message_id_list.append(scheduled_message_id)

        # Delete any leftover scheduled messages
        try:
            # Call the chat.scheduledMessages.list for list of messages
            result = client.chat_scheduledMessages_list(
            )

            # Print scheduled messages for deletion
            for message in range(len(result['scheduled_messages'])):
                try:
                    # Delete each message
                    result = client.chat_deleteScheduledMessage(
                        channel=result['scheduled_messages'][message]['channel_id'],
                        scheduled_message_id=result['scheduled_messages'][message]['id']
                    )
                    # Log the result
                    logger.info(result)

                except Exception as e:
                    logger.error(f"Error deleting scheduled message: {e}")
                    logger.info(message)

        except Exception as e:
            logger.error("Error creating conversation: {}".format(e))


        return
    if CLOCKIN_STATUS == 0:
        respond("You haven't clocked in yet today! Would you like to `/clockin?`")
        return

#----------------------------------------------------------------------------------------------------------------------------------------------#

# Notifications

SHIFT_NOTIFS = 1
WORK_NOTIFS = 1
FUN_NOTIFS = 1

# Open Notifications modal
@app.command("/notifications")
def notif_config(ack, body, client):
    # Acknowledge the command request
    ack()
    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "notif_configure",
            "title": {"type": "plain_text", "text": "Configure Notifications"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "This is where you can change your notifications to suit your needs. It is recommended that you turn on your break notifications so that you never forget to take some time to relax! \n\n _What sort of notifcations would you like to receive from me?_"
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": "https://i.pinimg.com/originals/71/1b/91/711b91643d47f43afe48d1e318f55b6a.png",
                        "alt_text": "Terry on the computer!"
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Notification Options:*"
                    },
                    "accessory": {
                        "type": "checkboxes",
                        "options": [
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Receive shift notifications from Terry Timebot."
                                },
                                "description": {
                                    "type": "mrkdwn",
                                    "text": "This includes break, shift start, and shift end notifications."
                                },
                                "value": "value-0"
                            },
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Receive work notifications from Terry Timebot."
                                },
                                "description": {
                                    "type": "mrkdwn",
                                    "text": "This includes calendar, meeting, and payslip notifications."
                                },
                                "value": "value-1"
                            },
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Receive fun notifications from Terry Timebot."
                                },
                                "description": {
                                    "type": "mrkdwn",
                                    "text": "This allows Terry to send you fun and interesting notifications such as news, holidays, and trivia."
                                },
                                "value": "value-2"
                            },
                        ],
                        "action_id": "notif-checkboxes"
                    },
                }
            ]
        }
    )

# Change notification settings based on user choice
@app.action("notif-checkboxes")
def change_notifs(ack, body, logger):
    global SHIFT_NOTIFS, WORK_NOTIFS, FUN_NOTIFS
    ack()
    logger.info(body)
    if "value" == "value-0":
        if SHIFT_NOTIFS == 0:
            SHIFT_NOTIFS = 1
            return
        if SHIFT_NOTIFS == 1:
            SHIFT_NOTIFS = 0
            return
        return
    if "value" == "value-1":
        if WORK_NOTIFS == 0:
            WORK_NOTIFS = 1
            return
        if WORK_NOTIFS == 1:
            WORK_NOTIFS = 0
            return
        return
    if "value" == "value-2":
        if FUN_NOTIFS == 0:
            FUN_NOTIFS = 1
            return
        if FUN_NOTIFS == 1:
            FUN_NOTIFS = 0
            return
        return

# Submit Notification Changes
@app.view("notif_configure")
def submit_notifs(ack, body, client, view, logger):
    global SHIFT_NOTIFS, WORK_NOTIFS, FUN_NOTIFS
    user = body["user"]["id"]
    stuff = view["state"]["values"]

    ack()

    if "value-0" in str(stuff):
        if SHIFT_NOTIFS == 0:
            SHIFT_NOTIFS = 1
            return
        if SHIFT_NOTIFS == 1:
            SHIFT_NOTIFS = 0
            return
        return
    if "value-1" in str(stuff):
        if WORK_NOTIFS == 0:
            WORK_NOTIFS = 1
            return
        if WORK_NOTIFS == 1:
            WORK_NOTIFS = 0
            return
        return
    if "value-2" in str(stuff):
        if FUN_NOTIFS == 0:
            FUN_NOTIFS = 1
            return
        if FUN_NOTIFS == 1:
            FUN_NOTIFS = 0
            return
        return

    ack()

    try:

        # Save to DB
        msg = ("Your notification changes were successful!" + str(stuff) + str(SHIFT_NOTIFS) + str(WORK_NOTIFS) + str(FUN_NOTIFS)) 
    except Exception as e:
        # Handle error
        msg = "There was an error with your changes. Please try again."

    # Message the user
    try:
        client.chat_postMessage(channel=user, text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")

#----------------------------------------------------------------------------------------------------------------------------------------------#

# See Shift Summaries
@app.shortcut("see_timesheets")
def see_timesheets(ack, body, client):
    # Acknowledge the command request
    ack()
    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "shift_summary",
            "title": {"type": "plain_text", "text": "Shift Summaries"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Your shift summaries are as follows:"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Next Shift:* Project Supervisor\nSunday, August 21 8:00am-4:30pm"
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": "https://api.slack.com/img/blocks/bkb_template_images/notifications.png",
                        "alt_text": "calendar thumbnail"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": "https://api.slack.com/img/blocks/bkb_template_images/notificationsWarningIcon.png",
                            "alt_text": "notifications warning icon"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Reminder: Next Follow-Up Meeting on September 4th*"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Previous Shifts:*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Last Shift:* " + clockin_time.strftime("%B, %d %Y: %I:%M %p") + " to " + clockout_time.strftime("%I:%M %p") + "\n*Total Time:* " + str(hours) + "hrs " + str(mins) + "mins " + "\nProject Supervisor"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "View Timesheet"
                        },
                        "action_id": "click_me_123"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Thursday, 18th August:* 8am to 3pm\nProject Supervisor"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "View Timesheet"
                        },
                        "action_id": "click_me_123"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Tuesday, 16th August:* 7am to 6:30pm\nProject Lead"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "View Timesheet"
                        },
                        "action_id": "click_me_123"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*<fakelink.ToMoreTimes.com|Show past timesheets>*"
                    }
                }
            ]
        }
    )

#----------------------------------------------------------------------------------------------------------------------------------------------#

# Unavailable Feature Page
@app.action("click_me_123")
def timesheet_buttons(ack, body, client, logger):
    ack()
    logger.info(body)
    client.views_push(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "Feature Unavailable"},
            "blocks": [
                {
                    "type": "image",
                    "image_url": "https://i.pinimg.com/originals/d1/7d/78/d17d78cd84a8d93a9a48274512e96162.gif",
                    "alt_text": "The picture did not load."
                },
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": "This feature is currently unavailable for the demo version of Terry Timebot. I'm awfully sorry about the inconvenience!"}
                },
            ]
        }
    )

#----------------------------------------------------------------------------------------------------------------------------------------------#


def ack_shortcut(ack):
    ack()

# Listen for a shortcut invocation
@app.shortcut("leave_request")
def leave_request(ack, body, client):
    # Acknowledge the command request
    ack()
    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "leave_req_submission",
            "title": {"type": "plain_text", "text": "Time Off Request"},
            "submit": {"type": "plain_text", "text": "Submit Request"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Which day/s would you like to request leave for?"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "datepicker",
                            "initial_date": "2022-01-01",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a date",
                                "emoji": True
                            },
                            "action_id": "start-date"
                        },
                        {
                            "type": "datepicker",
                            "initial_date": "2022-01-01",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a date",
                                "emoji": True
                            },
                            "action_id": "end-date"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "What kind of leave are you requesting?"
                    },
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a type",
                            "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Unpaid Leave",
                                    "emoji": True
                                },
                                "value": "value-0"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Sick and Carer's Leave",
                                    "emoji": True
                                },
                                "value": "value-1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Maternity/Paternity Leave",
                                    "emoji": True
                                },
                                "value": "value-2"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Annual Leave",
                                    "emoji": True
                                },
                                "value": "value-3"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Other (Please Specify Below)",
                                    "emoji": True
                                },
                                "value": "value-4"
                            }
                        ],
                        "action_id": "leave-type"
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "reason-input"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Please state a reason for this request. (Optional)",
                        "emoji": True
                    }
                },
            ]
        }
    )

@app.view("leave_req_submission")
def handle_submission(ack, body, client, view, logger):
    leaveType = view["state"]["values"]["leave-type"]["value"]
    leaveReason = view["state"]["values"]["reason-input"]
    leaveStart = view["start-date"]
    leaveEnd = view["end-date"]
    user = body["user"]["id"]
    # Validate the inputs
    errors = {}
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return
    # Acknowledge the view_submission request and close the modal
    ack()
    # Save input data to a DB
    # then sending the user verification of submission

    # Message to send user
    msg = ""
    try:
        # Save to DB
        msg = "Your submission  was successful!"
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission."

    # Message the user
    try:
        client.chat_postMessage(channel=user, text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")

#----------------------------------------------------------------------------------------------------------------------------------------------#


# Run Terry Timebot
if __name__ == "__main__":
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        handler.start()