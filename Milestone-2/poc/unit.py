#!/usr/bin/env python
import unittest
from app import readJson
import js


class TestApp(unittest.TestCase):


  def test_readJson(self):
  
    result = readJson("configs.json")
    self.assertIsNotNone(result)

   

if __name__ == "__main__":
   suite = unittest.TestLoader().loadTestsFromTestCase(TestApp)
   unittest.TextTestRunner(verbosity=2).run(suite)c
