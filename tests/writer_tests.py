"""
In this file tests for Writer scripts are gathered.
"""
import os
import tempfile
import unittest

import mock

from writer import XMLWriter, CSVWriter, WriterManager


class CSVWriterTest(unittest.TestCase):
    writer = CSVWriter

    def setUp(self):
        self.outfile_path = tempfile.mkstemp(suffix='.csv')[1]

    def tearDown(self):
        os.remove(self.outfile_path)

    def test_not_supported_ext(self):
        writer = self.writer('test.csvv')
        self.assertFalse(writer.check())

    def test_supported_ext(self):
        writer = self.writer('test.csv')
        self.assertTrue(writer.check())

    def test_save(self):
        writer = self.writer(self.outfile_path)
        writer.save(['abc', 'def', 'ghi'])
        expected = 'url\nabc\ndef\nghi\n'
        with open(self.outfile_path, 'rb') as result:
            self.assertEqual(result.read(), expected)


class XMLWriterTest(unittest.TestCase):
    writer = XMLWriter

    def setUp(self):
        self.outfile_path = tempfile.mkstemp(suffix='.xml')[1]

    def tearDown(self):
        os.remove(self.outfile_path)

    def test_unknown_ext(self):
        writer = self.writer('test.xxml')
        self.assertTrue(writer.check())
        self.assertEqual(writer.file_name, 'test.xxml.xml')

    def test_supported_ext(self):
        writer = self.writer('test.xml')
        self.assertTrue(writer.check())

    def test_save(self):
        writer = self.writer(self.outfile_path)
        writer.save(['1', '2', '3'])
        expected = '' \
           '<?xml version="1.0" encoding="UTF-8"?>\n' \
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' \
           '  <url>\n    <loc>1</loc>\n  </url>\n' \
           '  <url>\n    <loc>2</loc>\n  </url>\n' \
           '  <url>\n    <loc>3</loc>\n  </url>\n' \
           '</urlset>'
        with open(self.outfile_path, 'rt') as result:
            self.assertEqual(result.read(), expected)


class WriterManagerTest(unittest.TestCase):

    def test_select_csv_writer(self):
        manager = WriterManager('test.csv')
        self.assertTrue(isinstance(manager.writer, CSVWriter))

    def test_select_xml_writer(self):
        manager = WriterManager('test.xml')
        self.assertTrue(isinstance(manager.writer, XMLWriter))

    def test_select_xml_writer_by_default(self):
        manager = WriterManager('test.csvvv')
        self.assertTrue(isinstance(manager.writer, XMLWriter))

    @mock.patch.object(CSVWriter, 'save')
    def test_skip_writing_when_no_data(self, save):
        manager = WriterManager('test.csv')
        manager.export_data([])
        self.assertFalse(save.called)

    @mock.patch.object(CSVWriter, 'save')
    def test_writing_with_list(self, save):
        manager = WriterManager('test.csv')
        manager.export_data([1, 2, 3])
        self.assertTrue(save.called)
        self.assertItemsEqual(save.call_args_list[0][0][0], [1, 2, 3])

    @mock.patch.object(CSVWriter, 'save')
    def test_writing_with_tuple(self, save):
        manager = WriterManager('test.csv')
        manager.export_data((1, 2, 3))
        self.assertTrue(save.called)
        self.assertItemsEqual(save.call_args_list[0][0][0], [1, 2, 3])

    @mock.patch.object(CSVWriter, 'save')
    def test_writing_with_set(self, save):
        manager = WriterManager('test.csv')
        manager.export_data({1, 2, 3})
        self.assertTrue(save.called)
        self.assertItemsEqual(save.call_args_list[0][0][0], [1, 2, 3])

    @mock.patch.object(CSVWriter, 'save')
    def test_skip_writing_with_string(self, save):
        manager = WriterManager('test.csv')
        with self.assertRaises(AttributeError):
            manager.export_data('1, 2, 3')
        self.assertFalse(save.called)


if __name__ == '__main__':
    unittest.main()
