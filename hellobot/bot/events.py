from flask import app
import slack

from slackeventsapi import SlackEventAdapter


def start_bot(app, instance):
    event_handler = SlackEventAdapter(instance.singing, '/slack/events', app)
    client = slack.WebClient(instance.token)
    bot_id = client.api_call('auth.test')['user_id']

    return bot_id