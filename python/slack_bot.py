"""Code relating to sending alerts (Using slack)."""
import logging
from urllib.error import URLError

from slack_sdk.webhook import WebhookClient
from ... import SLACK_WEBHOOK_URL

from ... import classproperty

logger = logging.getLogger(__name__)

NO_WEBHOOK_WARNING_MESSAGE = "SLACK MSG THAT WOULD BE SENT:"


class FakeWebhookClient:
    """To be used instead of calling the actual slack, i.e.
    when using an invalid SLACK_WEBHOOK_URL (e.g.
    SLACK_WEBHOOK_URL = '' for testing on local / dev).
    Or if the slack URL fails for any reason."""

    @staticmethod
    def send(*args, **kwargs):
        logger.error(f"{NO_WEBHOOK_WARNING_MESSAGE} '{*args, kwargs}'")


class SlackBot(metaclass=classproperty.meta):
    """Slack class object. Does not need to be instantiated.
    Just call the SlackBot.send_slack_message("...").

    e.g.
    >>> SlackBot.send_slack_message("...")
    """

    def __init__(self):
        raise TypeError(
            "Do not instantiate SlackBot. Use it directly."
            "\n Don't do `slackbot = SlackBot(); slackbot.send_slack_message(...)`"
            "\n Directly do: `SlackBot.send_slack_message(...)`"
        )

    @classproperty
    def webhook_client(cls):
        """Creates the Slack webhook client if called for the first time.
        Otherwise uses the existing Slack webhook client."""
        if not hasattr(cls, "_webhook_client"):
            cls._webhook_client = WebhookClient(SLACK_WEBHOOK_URL)  # create the client
            try:
                cls._webhook_client.send_dict({"test": "test"})  # test the url works
            except Exception as exc:
                failed_due_to_bad_url = isinstance(exc, URLError) or isinstance(exc, ValueError)
                failing_msg = (
                    f"Unable to setup slack bot due to {'an invalid SLACK_WEBHOOK_URL' if failed_due_to_bad_url else exc}."
                    + "Falling back to logger."
                )
                failing_lvl = logging.WARNING if failed_due_to_bad_url else logging.ERROR
                logger.log(failing_lvl, failing_msg)
                cls._webhook_client = FakeWebhookClient()  # url doesn't work, use logger instead

        return cls._webhook_client

    @classmethod
    def send_slack_message(cls, message_text):
        response = cls.webhook_client.send(
            text="fallback",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message_text,
                    },
                }
            ],
        )
        return response

 #-------------------- tests ------------------#

from unittest.mock import MagicMock

import pytest


def test_send_slack_message_normal_behaviour(monkeypatch, cleanup_slackbot):
    """The patched version of sending a slack message
    i.e. if it actually used real credentials on a working server"""
    mocked_slack_webhook = MagicMock()
    monkeypatch.setattr(slack_alerts, "WebhookClient", mocked_slack_webhook)

    SlackBot.send_slack_message("Hello World")

    mocked_slack_webhook.assert_called_with(SLACK_WEBHOOK_URL)
    SlackBot.webhook_client.send.assert_called_once()


def test_patched_slack_message(monkeypatch, cleanup_slackbot, caplog):
    """Using an invalid SLACK_WEBHOOK_URL causes the fallback mechanism to occur
    i.e. uses logging instead."""
    monkeypatch.setattr(slack_alerts, "SLACK_WEBHOOK_URL", None)
    SlackBot.send_slack_message("Hello World!")
    assert issubclass(type(SlackBot._webhook_client), FakeWebhookClient)
    assert "Unable to setup slack bot due to an invalid SLACK_WEBHOOK_URL." in caplog.records[-2].message

    logged_msg = caplog.records[-1].message
    assert logged_msg.startswith(NO_WEBHOOK_WARNING_MESSAGE)
    assert "Hello World!" in logged_msg


def test_instantiating_slackbot_causes_error(cleanup_slackbot):
    with pytest.raises(TypeError):
        SlackBot()
