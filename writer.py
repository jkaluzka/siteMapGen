"""
Script contains writer class
"""
import logging
import xml.sax.saxutils

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

    def save(self, data):
        """
        Method for saving data into file.
        Each class that inherits must implement body of this method.

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

    def save(self, data):
        """
        Method save data into `csv` file.

        :param data: str[] - list of strings
        """
        with open(self.file_name, 'w') as csv_file:
            csv_file.writelines('url\n')
            for row in data:
                csv_file.writelines(row + '\n')


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
        if not self.file_name.endswith('.xml'):
            _logger.info('Unknown extension, `xml` will be used.')
            self.file_name += '.xml'
        return True

    def save(self, data):
        """
        Method save data in `xml` format.

        :param data: str[] - list of strings
        """
        header = '<?xml version="1.0" encoding="UTF-8"?>\n' \
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        with open(self.file_name, 'wt') as xml_file:
            xml_file.write(header)
            for row in data:
                xml_file.write('\n  <url>\n    <loc>%s</loc>\n  </url>' % (
                    xml.sax.saxutils.escape(row)))
            xml_file.write('\n</urlset>')


class WriterManager:
    """
    Writer manager that selects proper writer according to the extension.
    `XMLWriter` is the default one, when extension is unknown.
    """

    def __init__(self, file_name):
        for writer_class in (CSVWriter, XMLWriter):
            writer = writer_class(file_name)
            if writer.check():
                self.writer = writer
                break

        if not self.writer:
            raise ValueError('No writer was found!! - see check methods!')

    def export_data(self, data):
        """
        Call `save` method on writer. If no data was provided,
        warning will be logged.

        :param data: str[] - list of strings to save to file
        """
        if not data:
            _logger.warning('Empty data was passed to save function! Pass')
            return

        if not isinstance(data, (list, tuple, set)):
            raise AttributeError('Wrong type was passed as `data`: {}'.format(
                type(data)
            ))
        self.writer.save(data)
