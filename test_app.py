import unittest

class SampleTest(unittest.TestCase):
	def test_sample(self):
		self.assertEqual(1, 1)


import xmlrunner

if __name__ == '__main__':
	unittest.main(
		testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
		failfast=False, buffer=False, catchbreak=False)
