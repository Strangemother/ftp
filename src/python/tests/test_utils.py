from server.utils import key_generator, get_settings, Config
import unittest


class TestFTPMethods(unittest.TestCase):

    def test_key_generator(self):
        '''
        key_generator returns correct string
        '''
        k = key_generator()
        self.assertEqual(len(k), 43)
        self.assertIsInstance(k, (str,))

    def test_get_settings(self):
        '''
        get_settings returns config class from file
        '''
        c = get_settings('config.json')
        self.assertTrue(c.version, '0.1')

    def test_config_class(self):
        '''
        Generate an instance of the Config class to store config objects
        '''
        c = Config('config.json')
        self.assertIsNotNone(c._config)
        self.assertTrue(c.get('version'), '0.1')
