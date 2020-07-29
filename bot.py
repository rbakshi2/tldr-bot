# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import re



class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        LANGUAGE = "english"
        SENTENCES_COUNT = 3
        text = turn_context.activity.text
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        sentence_count_regex = re.compile(r'tldr-\d')
        mo = sentence_count_regex.search(text.lower())
        if mo and mo.group():
            tokens = mo.group().split('-')
            if len(tokens) == 2:
                SENTENCES_COUNT = tokens[1]
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        summary = ""
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            summary += str(sentence)
            summary += '\n'
        await turn_context.send_activity("tl;dr: " +  summary)
