#!C:\Users\SSAFY\Desktop\새 폴더 (2)\S09P22B201\backend\ssak3\venv\Scripts\python.exe

# $Id: rst2odt.py 9115 2022-07-28 17:06:24Z milde $
# Author: Dave Kuhlman <dkuhlman@rexx.com>
# Copyright: This module has been placed in the public domain.

"""
A front end to the Docutils Publisher, producing OpenOffice documents.
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except Exception:
    pass

from docutils.core import publish_cmdline_to_binary, default_description
from docutils.writers.odf_odt import Writer, Reader


description = ('Generates OpenDocument/OpenOffice/ODF documents from '
               'standalone reStructuredText sources.  ' + default_description)


writer = Writer()
reader = Reader()
output = publish_cmdline_to_binary(reader=reader, writer=writer,
                                   description=description)
