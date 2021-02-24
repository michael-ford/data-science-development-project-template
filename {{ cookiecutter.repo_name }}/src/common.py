#!/usr/bin/env python
import os, sys
import tempfile
import logbook, logbook.more


log = logbook.Logger('{{ cookiecutter.project_name }}')
def initialize_logger(console_level='INFO', log_file_path=None, overwrite=False, log_file_level='DEBUG'):
    """ Sets up logbook
    
    Args:
        console_level (str):        Debug level to print to console
        log_file_path (str):        Path to write log file to. If none does not write a log file.
        overwrite (bool):           If True overwrites log file.
        log_file_level (str):       Debug level to write to log file
    """
    LOG_FORMAT = '{record.message}'
    if log_file_path:
        log_file_path = log_file_path+'.log'
        if os.path.exists(log_file_path):
            if overwrite: 
                os.remove(log_file_path)
            else:
                raise IOError('File exists at provided log path')

        handler = logbook.NestedSetup([logbook.NullHandler(),
                                    logbook.FileHandler(log_file_path, level='DEBUG', format_string=LOG_FORMAT),
                                    logbook.more.ColorizedStderrHandler(format_string=LOG_FORMAT, level='INFO', bubble=True)])
    else:
        handler = logbook.NestedSetup([logbook.NullHandler(),
                                    logbook.more.ColorizedStderrHandler(format_string=LOG_FORMAT, level='INFO', bubble=True)])

    handler.push_application()


def markdown_table(header, data, transpose=False):
    '''Returns a string with table in markdown format
    Args
        header []           iterable of the header fields
        data []             iterable of data values (if 1 column) or of iterables containing column values (if > 1 column)
        transpose           transposes the table
    '''
    def table(header, data):
        result = []
        s = '|'+' | '.join(['{}'] * len(header))+'|'
        p = lambda x: s.format(*[str(i) for i in x])
        result.extend(list(map(p, (header if not isinstance(header[0], str) else [header]))))
        result.append('|'+('--|'*len(header)))
        if (not hasattr(data[0], '__iter__') or isinstance(data[0], str)):
            data = [[x] for x in data]
        result.extend(list(map(p, data)))
        return '\n'.join(result)

    if transpose:
        combined = [header] + data
        transposed = list(zip(*combined))
        return table(transposed[0], transposed[1:])
    
    return table(header, data)

def latex_table(header, data, transpose=False):
    def print_table(header, data):
        s = ' & '.join(['{: <20}'] * len(data[0])) + '\\\\'
        p = lambda x: print(s.format(*[str(i) for i in x]))
        print('\\hline')
        map(p, (header if not isinstance(header[0], str) else [header]))
        print('\\hline')
        map(p, data)
        print('\\hline')
    
    if transpose:
        combined = [header] + data
        transposed = list(zip(*combined))
        print_table(transposed[0], transposed[1:])
    else:
        print_table(header, data)
