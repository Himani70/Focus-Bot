import unittest
#function to be tested
def add(a, b):
    return a + b
class FooTestCase(unittest.TestCase):
    # test method       
    def test_add(self):
        sum = add(1, 2)
        # validate the result of the code we're testing.
        self.assertEqual(3, sum)
    def test_add_negative_numbers(self):                                                                                                                                                                                                                                  
        sum = add(-1, -2)                                                                                                                                                                                                                                                 
        self.assertEqual(-3, sum)


    
