"""
Script contains writer class
"""
import collections
import csv
import xml.sax.saxutils

import logging

logging.basicConfig()
_logger = logging.getLogger(__name__)


class Writer:
    """
    Writer class implements methods that allow user
    to export data to `csv` or `xml` file.
    """

    def __init__(self, file_name):
        """
        :param file_name: str - name of the file
        """
        self.file_name = file_name

    def check(self):
        """
        Method checks if class can handle provided extension.
        Each class that inherits must implement body of this method.

        :file_name: str - name of the file
        :return: bool - can handle extension or not 
        """
        raise NotImplementedError

    def save(self, file_name, data):
        """
        Method for saving data into file.
        Each class that inherits must implement body of this method.

        :param file_name: str - name of the output file
        :param data: str[] - list of strings
        """
        raise NotImplementedError


class CSVWriter(Writer):
    """
    Implementation of CSVWriter
    """

    def check(self):
        """
        Method checks if class can save `csv` file.

        :file_name: str - name of the file
        :return: bool - can handle extension or not
        """
        return self.file_name.endswith('.csv')

    def save(self, file_name, data):
        """
        Method save data into `csv` file.

        :param file_name: str - name of the output file
        :param data: str[] - list of strings
        """
        with open(file_name, 'wb') as csv_file:
            file_writer = csv.writer(
                csv_file,
                delimiter=',',
                lineterminator='\n',
            )
            file_writer.writerow(['url'])
            for row in data:
                file_writer.writerow(row)


class XMLWriter(Writer):
    """
    Implementation of XMLWriter
    """

    def check(self):
        """
        Method checks if class can save `xml` file.

        :file_name: str - name of the file
        :return: bool - can handle extension or not
        """
        return self.file_name.endswith('.xml')

    def save(self, file_name, data):
        """
        Method save data in `xml` format.

        :param file_name: str - name of the output file
        :param data: str[] - list of strings
        """
        header = '<?xml version="1.0" encoding="UTF-8"?>\n' \
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        with open(file_name, 'wt') as fh:
            fh.write(header)
            for row in data:
                fh.write('\n  <url>\n    <loc>%s</loc>\n  </url>' % (
                    xml.sax.saxutils.escape(row)))
            fh.write('\n</urlset>')


class WriterManager:
    """
    Writer manager that selects proper writer according to the extension.
    `XMLWriter` is the default one, when extension is unknown.
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self.writer = CSVWriter(file_name)
        if not self.writer.check():
            self.writer = XMLWriter(file_name)
            if not self.writer.check():
                self.file_name += '.xml'

    def export_data(self, data):
        """
        Call `save` method on writer. If no data was provided,
        warning will be logged.

        :param data: str[] - list of strings to save to file
        """
        if not data:
            _logger.warning('Empty data was passed to save function! Pass')
            return

        if not isinstance(data, collections.Sequence) or isinstance(data, str):
            raise AttributeError('Wrong type was passed as `data`')
        self.writer.save(self.file_name, data)
