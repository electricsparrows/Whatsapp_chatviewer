from gui import *

def get_test_data1():
    data = [{'msg_id': 19, 'conv_id': None, 'import_ref': 1,
             'date_time': '2015-11-20 18:12:00', 'speaker_name': 'molly',
             'msg_content': 'this is a business world, ppl hv to think of some excuse to spend money',
             'msg_notes': None},
            {'msg_id': 124, 'conv_id': None, 'import_ref': 1,
             'date_time': '2015-11-21 11:24:00', 'speaker_name': 'molly',
             'msg_content': 'Singaporeans just do business',
             'msg_notes': "some note"},
            {'msg_id': 1819, 'conv_id': None, 'import_ref': 1,
             'date_time': '2015-11-26 14:19:00', 'speaker_name': 'molly',
             'msg_content': 'to do mini enterprise, u need business knowledge',
             'msg_notes': None},
            {'msg_id': 1822, 'conv_id': None, 'import_ref': 1,
             'date_time': '2015-11-26 14:20:00', 'speaker_name': 'crystal',
             'msg_content': 'But business is part of the course', 'msg_notes': "2465xw"},
            {'msg_id': 5312, 'conv_id': None, 'import_ref': 1,
             'date_time': '2016-01-13 15:21:00', 'speaker_name': 'crystal',
             'msg_content': 'I meant to say that my phone number is out of business right now',
             'msg_notes': None}]
    return data

def test_make_table():
    assert False


def test_update_summary():
    assert False


def test_get_messages():
    assert False


def test_render_messages():
    data = get_test_data1()
    rv = render_messages(data)


def test_reformat_records():
    data = get_test_data1()
    rv = reformat_records(data)
    assert rv[0] == [19, "18:12", "molly", "this is a business world, ppl hv to think of some excuse to spend money", None]
    assert rv[1] == [124, "11:24", "molly", "Singaporeans just do business", "some note"]
    assert rv[2] == [1819, "14:19", "molly", "to do mini enterprise, u need business knowledge", None]
    assert rv[3] == [1822, "14:20", "crystal", "But business is part of the course", "2465xw"]
    assert rv[4] == [5312, "15:21", "crystal", "I meant to say that my phone number is out of business right now", None]
