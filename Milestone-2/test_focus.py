import unittest
from rtm import processMessage
import json

# channel_id = None
# tokens = None
# slack_client = None
# jira = None
# db = None
# filePath = 'configs.json'
# with open(filePath) as json_data:
#     tokens = json.load(json_data)
#     tokens["test"] = True
#function to be tested
# def add(a, b):
#     return a + b
class FooTestCase(unittest.TestCase):
    # test method
    # test_describe_commands_positive
    data = {}
    data['type'] = 'message'
    data['channel'] = 'xxxx'

    def test_case_1_describe_commands(self):
        # data = {}
        # data['type'] = 'message'
        self.data['text'] = '<@UPMT8NZJS> describe commands'
        self.data['user'] = 'xxxx'
        # data['channel'] = 'xxxx'
        r = processMessage(self.data, True)
        response = r.response[0].decode('utf-8')
        self.assertIn('Command', response)

    def test_case_2_describe_commands(self):
        # data = {}
        # data['type'] = 'message'
        self.data['text'] = 'describe commands'
        self.data['user'] = 'xxxx'
        # data['channel'] = 'xxxx'
        r = processMessage(self.data, True)
        response = r.response[0].decode('utf-8')
        self.assertEqual('Invalid command format', response)

    def test_case_1_list_tasks(self):
        self.data['text'] = '<@UPMT8NZJS> list tasks'
        self.data['user'] = 'pbhalas'
        # data['channel'] = 'xxxx'
        r = processMessage(self.data, True)
        response = r.response[0].decode('utf-8')
        self.assertIn('Project', response)

    def test_case_2_list_tasks(self):
        self.data['text'] = '<@UPMT8NZJS> list tasks'
        self.data['user'] = 'xxxx'
        # data['channel'] = 'xxxx'
        r = processMessage(self.data, True)
        response = r.response[0].decode('utf-8')
        self.assertIn('No Active Tasks exist!', response)

    def test_case_3_list_tasks(self):
        self.data['text'] = 'list tasks'
        self.data['user'] = 'xxxx'
        r = processMessage(self.data, True)
        response = r.response[0].decode('utf-8')
        self.assertEqual('Invalid command format', response)

    def test_case_1_create_task(self):
        self.data['text'] = '<@UPMT8NZJS> create task SF sample_task sample_task_description '
        self.data['user'] = 'xxxx'
        r = processMessage(self.data, True)
        response = r.response[0].decode('utf-8')
        self.assertIn('Insufficient', response)

    def test_case_2_create_task(self):
        self.data['text'] = '<@UPMT8NZJS> create task SF issue sample_task sample_task_description'
        self.data['user'] = 'xxxx'
        r = processMessage(self.data, True)
        response = r.response[0].decode('utf-8')
        self.assertIn('Insufficient', response)

    def test_case_3_create_task(self):
        self.data['text'] = '<@UPMT8NZJS> create task SF task sample_task sample_task_description 6 8'
        self.data['user'] = 'xxxx'
        r = processMessage(self.data, True)
        response = r.response[0].decode('utf-8')
        self.assertIn('Too many', response)

    def test_case_4_create_task(self):
        self.data['text'] = 'create task SF task sample_task sample_task_description 6'
        self.data['user'] = 'xxxx'
        r = processMessage(self.data, True)
        response = r.response[0].decode('utf-8')
        self.assertEqual('Invalid command format', response)

    # def test_add(self):
    #     sum = add(1, 2)
    #     # validate the result of the code we're testing.
    #     self.assertEqual(3, sum)
    # def test_add_negative_numbers(self):
    #     sum = add(-1, -2)
    #     self.assertEqual(-3, sum)


if __name__ == "__main__":
   suite = unittest.TestLoader().loadTestsFromTestCase(FooTestCase)
   unittest.TextTestRunner(verbosity=2).run(suite)


