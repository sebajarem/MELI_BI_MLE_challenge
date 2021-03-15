""" Tests to validate that the autocompleter functions correctly.
    We are evaluating how you write unit tests, so please demonstrate your ability at writing
    good tests.  Feel free to add more tests to validate your solution. """

import pytest
import autocompleter
import pandas as pd

def test_conversations_agent_1(df_conversations_agent, df_conversations):
    ac = autocompleter.Autocompleter()
    ac.conversations = df_conversations
    actual = ac.conversations_agent()
    expected = df_conversations_agent
    pd.testing.assert_frame_equal(actual, expected)


@pytest.mark.parametrize(
    "prefix",
    [
        ('what is'),
        ('i am'),
        ('wh'),
        ('where')
    ]
)
def test_generate_completions(prefix):
    myauto = autocompleter.Autocompleter.load()

    for frase in myauto.generate_completions(prefix):
        assert frase[:len(prefix)] == prefix



## fixtures

@pytest.fixture()
def df_conversations():
    return pd.DataFrame(
        {'IssueId': {0: '1',
                     1: '1',
                     2: '10001',
                     3: '10001',
                     4: '10001',
                     5: '20001',
                     6: '20001',
                     7: '20001',
                     8: '30001',
                     9: '30001',
                     10: '30001',
                     11: '30001',
                     12: '30001',
                     13: '30001',
                     14: '30001',
                     15: '30001',
                     16: '30001',
                     17: '30001',
                     18: '30001',
                     19: '30001'},
         'CompanyGroupId': {0: '1',
                            1: '1',
                            2: '1',
                            3: '1',
                            4: '1',
                            5: '1',
                            6: '1',
                            7: '1',
                            8: '40001',
                            9: '40001',
                            10: '40001',
                            11: '40001',
                            12: '40001',
                            13: '40001',
                            14: '40001',
                            15: '40001',
                            16: '40001',
                            17: '40001',
                            18: '40001',
                            19: '40001'},
         'IsFromCustomer': {0: True,
                            1: True,
                            2: True,
                            3: True,
                            4: True,
                            5: True,
                            6: True,
                            7: True,
                            8: True,
                            9: False,
                            10: True,
                            11: False,
                            12: True,
                            13: False,
                            14: False,
                            15: True,
                            16: False,
                            17: False,
                            18: False,
                            19: True},
         'Text': {0: "Hi! I placed an order on your website and I can't find the tracking number. Can you help me find out where my package is?",
                  1: 'I think I used my email address to log in.',
                  2: 'My battery exploded!',
                  3: "It's on fire, it's melting the carpet!",
                  4: 'What should I do!',
                  5: "I'm interested in upgrading my plan.",
                  6: 'Can you tell me a bit about Prime?',
                  7: 'My friend has it, and it seems like a great deal',
                  8: 'Hello',
                  9: 'Hello Werner how may I help you today?',
                  10: 'I have recently moved to a new apartment and would like to update my contact details',
                  11: 'Sure I can help you with that? Could you please provide me with your new address?',
                  12: 'Ok, 5 Seaman Ave, Apt 3F, New York, New York, 10034',
                  13: 'Let me update that information on our system',
                  14: 'OK Wernzio, I have updated your address to the system',
                  15: 'Great, thank. I also need to place a order for a new installation as the place I live currently does not have the required wiring',
                  16: 'Ok let me go ahead and request a work order for a new installation. Give me a moment...',
                  17: 'OK a installation order has been places. Seems the earilest we will be able to help you  is from the 20th February onwards',
                  18: 'does that suite you?',
                  19: 'Yes. It soes'}}
    )


@pytest.fixture()
def df_conversations_agent():
    return pd.DataFrame(
        {'index': {0: 9, 1: 11, 2: 13, 3: 14, 4: 16, 5: 17, 6: 18},
         'Text': {0: 'Hello Werner how may I help you today?',
                  1: 'Sure I can help you with that? Could you please provide me with your new address?',
                  2: 'Let me update that information on our system',
                  3: 'OK Wernzio, I have updated your address to the system',
                  4: 'Ok let me go ahead and request a work order for a new installation. Give me a moment...',
                  5: 'OK a installation order has been places. Seems the earilest we will be able to help you  is from the 20th February onwards',
                  6: 'does that suite you?'}}
    )
