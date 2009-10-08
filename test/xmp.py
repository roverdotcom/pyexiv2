# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2009 Olivier Tilloy <olivier@tilloy.net>
#
# This file is part of the pyexiv2 distribution.
#
# pyexiv2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# pyexiv2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyexiv2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301 USA.
#
# Author: Olivier Tilloy <olivier@tilloy.net>
#
# ******************************************************************************

import unittest
from pyexiv2 import XmpTag, XmpValueError, FixedOffset
import datetime


class ImageMetadataMock(object):

    tags = {}

    def _set_xmp_tag_value(self, key, value):
        self.tags[key] = value

    def _delete_xmp_tag(self, key):
        try:
            del self.tags[key]
        except KeyError:
            pass


class TestXmpTag(unittest.TestCase):

    def test_convert_to_python_bag(self):
        xtype = 'bag Text'
        # Valid values
        self.assertEqual(XmpTag._convert_to_python('', xtype), [])
        self.assertEqual(XmpTag._convert_to_python('One value only', xtype), [u'One value only'])
        self.assertEqual(XmpTag._convert_to_python('Some, text, keyword, this is a test', xtype),
                         [u'Some', u'text', u'keyword', u'this is a test'])

    def test_convert_to_string_bag(self):
        xtype = 'bag Text'
        # Valid values
        self.assertEqual(XmpTag._convert_to_string([], xtype), '')
        self.assertEqual(XmpTag._convert_to_string(['One value only'], xtype), 'One value only')
        self.assertEqual(XmpTag._convert_to_string([u'One value only'], xtype), 'One value only')
        self.assertEqual(XmpTag._convert_to_string([u'Some', u'text', u'keyword', u'this is a test'], xtype),
                         'Some, text, keyword, this is a test')
        self.assertEqual(XmpTag._convert_to_string(['Some   ', '  text    '], xtype),
                         'Some   ,   text    ')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, 'invalid', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, [1, 2, 3], xtype)

    def test_convert_to_python_boolean(self):
        xtype = 'Boolean'
        # Valid values
        self.assertEqual(XmpTag._convert_to_python('True', xtype), True)
        self.assertEqual(XmpTag._convert_to_python('False', xtype), False)
        # Invalid values: not converted
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, 'invalid', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, None, xtype)

    def test_convert_to_string_boolean(self):
        xtype = 'Boolean'
        # Valid values
        self.assertEqual(XmpTag._convert_to_string(True, xtype), 'True')
        self.assertEqual(XmpTag._convert_to_string(False, xtype), 'False')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, 'invalid', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, None, xtype)

    def test_convert_to_python_date(self):
        xtype = 'Date'
        # Valid values
        self.assertEqual(XmpTag._convert_to_python('1999', xtype),
                         datetime.date(1999, 1, 1))
        self.assertEqual(XmpTag._convert_to_python('1999-10', xtype),
                         datetime.date(1999, 10, 1))
        self.assertEqual(XmpTag._convert_to_python('1999-10-13', xtype),
                         datetime.date(1999, 10, 13))
        self.assertEqual(XmpTag._convert_to_python('1999-10-13T05:03Z', xtype) - \
                         datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset()),
                         datetime.timedelta(0))
        self.assertEqual(XmpTag._convert_to_python('1999-10-13T05:03+06:00', xtype) - \
                         datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset('+', 6, 0)),
                         datetime.timedelta(0))
        self.assertEqual(XmpTag._convert_to_python('1999-10-13T05:03-06:00', xtype) - \
                         datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset('-', 6, 0)),
                         datetime.timedelta(0))
        self.assertEqual(XmpTag._convert_to_python('1999-10-13T05:03:54Z', xtype) - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, tzinfo=FixedOffset()),
                         datetime.timedelta(0))
        self.assertEqual(XmpTag._convert_to_python('1999-10-13T05:03:54+06:00', xtype) - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, tzinfo=FixedOffset('+', 6, 0)),
                         datetime.timedelta(0))
        self.assertEqual(XmpTag._convert_to_python('1999-10-13T05:03:54-06:00', xtype) - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, tzinfo=FixedOffset('-', 6, 0)),
                         datetime.timedelta(0))
        self.assertEqual(XmpTag._convert_to_python('1999-10-13T05:03:54.721Z', xtype) - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, 721000, tzinfo=FixedOffset()),
                         datetime.timedelta(0))
        self.assertEqual(XmpTag._convert_to_python('1999-10-13T05:03:54.721+06:00', xtype) - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, 721000, tzinfo=FixedOffset('+', 6, 0)),
                         datetime.timedelta(0))
        self.assertEqual(XmpTag._convert_to_python('1999-10-13T05:03:54.721-06:00', xtype) - \
                         datetime.datetime(1999, 10, 13, 5, 3, 54, 721000, tzinfo=FixedOffset('-', 6, 0)),
                         datetime.timedelta(0))
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, 'invalid', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, '11/10/1983', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, '-1000', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, '2009-13', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, '2009-10-32', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, '2009-10-30T25:12Z', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, '2009-10-30T23:67Z', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, '2009-01-22T21', xtype)

    def test_convert_to_string_date(self):
        xtype = 'Date'
        # Valid values
        self.assertEqual(XmpTag._convert_to_string(datetime.date(2009, 2, 4), xtype),
                         '2009-02-04')
        self.assertEqual(XmpTag._convert_to_string(datetime.datetime(1999, 10, 13), xtype),
                         '1999-10-13')
        self.assertEqual(XmpTag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset()), xtype),
                         '1999-10-13T05:03Z')
        self.assertEqual(XmpTag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset('+', 5, 30)), xtype),
                         '1999-10-13T05:03+05:30')
        self.assertEqual(XmpTag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, tzinfo=FixedOffset('-', 11, 30)), xtype),
                         '1999-10-13T05:03-11:30')
        self.assertEqual(XmpTag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, tzinfo=FixedOffset()), xtype),
                         '1999-10-13T05:03:27Z')
        self.assertEqual(XmpTag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, tzinfo=FixedOffset('+', 5, 30)), xtype),
                         '1999-10-13T05:03:27+05:30')
        self.assertEqual(XmpTag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, tzinfo=FixedOffset('-', 11, 30)), xtype),
                         '1999-10-13T05:03:27-11:30')
        self.assertEqual(XmpTag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, 124300, tzinfo=FixedOffset()), xtype),
                         '1999-10-13T05:03:27.1243Z')
        self.assertEqual(XmpTag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, 124300, tzinfo=FixedOffset('+', 5, 30)), xtype),
                         '1999-10-13T05:03:27.1243+05:30')
        self.assertEqual(XmpTag._convert_to_string(datetime.datetime(1999, 10, 13, 5, 3, 27, 124300, tzinfo=FixedOffset('-', 11, 30)), xtype),
                         '1999-10-13T05:03:27.1243-11:30')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, 'invalid', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, None, xtype)

    def test_convert_to_python_integer(self):
        xtype = 'Integer'
        # Valid values
        self.assertEqual(XmpTag._convert_to_python('23', xtype), 23)
        self.assertEqual(XmpTag._convert_to_python('+5628', xtype), 5628)
        self.assertEqual(XmpTag._convert_to_python('-4', xtype), -4)
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, 'abc', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, '5,64', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, '47.0001', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, '1E3', xtype)

    def test_convert_to_string_integer(self):
        xtype = 'Integer'
        # Valid values
        self.assertEqual(XmpTag._convert_to_string(123, xtype), '123')
        self.assertEqual(XmpTag._convert_to_string(-57, xtype), '-57')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, 'invalid', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, 3.14, xtype)

    def test_convert_to_python_langalt(self):
        xtype = 'Lang Alt'
        # Valid values
        self.assertEqual(XmpTag._convert_to_python('lang="x-default" some text', xtype),
                         {'x-default': u'some text'})
        self.assertEqual(XmpTag._convert_to_python('lang="x-default" some text, lang="fr-FR" du texte', xtype),
                         {'x-default': u'some text', 'fr-FR': u'du texte'})
        self.assertEqual(XmpTag._convert_to_python('lang="x-default" some text   ,    lang="fr-FR"   du texte  ', xtype),
                         {'x-default': u'some text   ', 'fr-FR': u'  du texte  '})
        self.assertEqual(XmpTag._convert_to_python('lang="x-default" some text, lang="fr-FR" du texte, lang="es-ES" un texto', xtype),
                         {'x-default': u'some text', 'fr-FR': u'du texte', 'es-ES': u'un texto'})
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, 'invalid', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, 'lang="malformed', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, 'xlang="x-default" some text', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, 'lang="x-default" some text, xlang="fr-FR" du texte', xtype)

    def test_convert_to_string_langalt(self):
        xtype = 'Lang Alt'
        # Valid values
        self.assertEqual(XmpTag._convert_to_string({'x-default': 'some text'}, xtype),
                         'lang="x-default" some text')
        self.assertEqual(XmpTag._convert_to_string({'x-default': u'some text'}, xtype),
                         'lang="x-default" some text')
        self.assertEqual(XmpTag._convert_to_string({'x-default': 'some text', 'fr-FR': 'du texte'}, xtype),
                         'lang="x-default" some text, lang="fr-FR" du texte')
        self.assertEqual(XmpTag._convert_to_string({'x-default': u'some text', 'fr-FR': 'du texte'}, xtype),
                         'lang="x-default" some text, lang="fr-FR" du texte')
        self.assertEqual(XmpTag._convert_to_string({'x-default': u'some text', 'fr-FR': 'du texte', 'es-ES': 'un texto'}, xtype),
                         'lang="x-default" some text, lang="es-ES" un texto, lang="fr-FR" du texte')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, 'invalid', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, {}, xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, {'x-default': 25}, xtype)

    def test_convert_to_python_mimetype(self):
        xtype = 'MIMEType'
        # Valid values
        self.assertEqual(XmpTag._convert_to_python('image/jpeg', xtype),
                         {'type': 'image', 'subtype': 'jpeg'})
        self.assertEqual(XmpTag._convert_to_python('video/ogg', xtype),
                         {'type': 'video', 'subtype': 'ogg'})
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, 'invalid', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, 'image-jpeg', xtype)

    def test_convert_to_string_mimetype(self):
        xtype = 'MIMEType'
        # Valid values
        self.assertEqual(XmpTag._convert_to_string({'type': 'image', 'subtype': 'jpeg'}, xtype), 'image/jpeg')
        self.assertEqual(XmpTag._convert_to_string({'type': 'video', 'subtype': 'ogg'}, xtype), 'video/ogg')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, 'invalid', xtype)
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, {'type': 'image'}, xtype)

    def test_convert_to_python_propername(self):
        xtype = 'ProperName'
        # Valid values
        self.assertEqual(XmpTag._convert_to_python('Gérard', xtype), u'Gérard')
        self.assertEqual(XmpTag._convert_to_python('Python Software Foundation', xtype), u'Python Software Foundation')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, None, xtype)

    def test_convert_to_string_propername(self):
        xtype = 'ProperName'
        # Valid values
        self.assertEqual(XmpTag._convert_to_string('Gérard', xtype), 'Gérard')
        self.assertEqual(XmpTag._convert_to_string(u'Gérard', xtype), 'Gérard')
        self.assertEqual(XmpTag._convert_to_string(u'Python Software Foundation', xtype), 'Python Software Foundation')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, None, xtype)

    def test_convert_to_python_text(self):
        xtype = 'Text'
        # Valid values
        self.assertEqual(XmpTag._convert_to_python('Some text.', xtype), u'Some text.')
        self.assertEqual(XmpTag._convert_to_python('Some text with exotic chàräctérʐ.', xtype),
                         u'Some text with exotic chàräctérʐ.')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_python, None, xtype)

    def test_convert_to_string_text(self):
        xtype = 'Text'
        # Valid values
        self.assertEqual(XmpTag._convert_to_string(u'Some text', xtype), 'Some text')
        self.assertEqual(XmpTag._convert_to_string(u'Some text with exotic chàräctérʐ.', xtype),
                         'Some text with exotic chàräctérʐ.')
        self.assertEqual(XmpTag._convert_to_string('Some text with exotic chàräctérʐ.', xtype),
                         'Some text with exotic chàräctérʐ.')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, None, xtype)

    def test_convert_to_python_uri(self):
        xtype = 'URI'
        # Valid values
        self.assertEqual(XmpTag._convert_to_python('http://example.com', xtype), 'http://example.com')
        self.assertEqual(XmpTag._convert_to_python('https://example.com', xtype), 'https://example.com')
        self.assertEqual(XmpTag._convert_to_python('http://localhost:8000/resource', xtype),
                         'http://localhost:8000/resource')
        self.assertEqual(XmpTag._convert_to_python('uuid:9A3B7F52214211DAB6308A7391270C13', xtype),
                         'uuid:9A3B7F52214211DAB6308A7391270C13')

    def test_convert_to_string_uri(self):
        xtype = 'URI'
        # Valid values
        self.assertEqual(XmpTag._convert_to_string('http://example.com', xtype), 'http://example.com')
        self.assertEqual(XmpTag._convert_to_string(u'http://example.com', xtype), 'http://example.com')
        self.assertEqual(XmpTag._convert_to_string('https://example.com', xtype), 'https://example.com')
        self.assertEqual(XmpTag._convert_to_string('http://localhost:8000/resource', xtype),
                         'http://localhost:8000/resource')
        self.assertEqual(XmpTag._convert_to_string('uuid:9A3B7F52214211DAB6308A7391270C13', xtype),
                         'uuid:9A3B7F52214211DAB6308A7391270C13')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, None, xtype)

    def test_convert_to_python_url(self):
        xtype = 'URL'
        # Valid values
        self.assertEqual(XmpTag._convert_to_python('http://example.com', xtype), 'http://example.com')
        self.assertEqual(XmpTag._convert_to_python('https://example.com', xtype), 'https://example.com')
        self.assertEqual(XmpTag._convert_to_python('http://localhost:8000/resource', xtype),
                         'http://localhost:8000/resource')

    def test_convert_to_string_url(self):
        xtype = 'URL'
        # Valid values
        self.assertEqual(XmpTag._convert_to_string('http://example.com', xtype), 'http://example.com')
        self.assertEqual(XmpTag._convert_to_string(u'http://example.com', xtype), 'http://example.com')
        self.assertEqual(XmpTag._convert_to_string('https://example.com', xtype), 'https://example.com')
        self.assertEqual(XmpTag._convert_to_string('http://localhost:8000/resource', xtype),
                         'http://localhost:8000/resource')
        # Invalid values
        self.failUnlessRaises(XmpValueError, XmpTag._convert_to_string, None, xtype)

    # TODO: other types


    def test_set_value_no_metadata(self):
        tag = XmpTag('Xmp.xmp.ModifyDate', 'ModifyDate', 'Modify Date',
                     'The date and time the resource was last modified. Note:' \
                     ' The value of this property is not necessarily the same' \
                     "as the file's system modification date because it is " \
                     'set before the file is saved.', 'Date',
                     '2005-09-07T15:09:51-07:00')
        old_value = tag.value
        tag.value = datetime.datetime(2009, 4, 22, 8, 30, 27, tzinfo=FixedOffset())
        self.failIfEqual(tag.value, old_value)

    def test_set_value_with_metadata(self):
        tag = XmpTag('Xmp.xmp.ModifyDate', 'ModifyDate', 'Modify Date',
                     'The date and time the resource was last modified. Note:' \
                     ' The value of this property is not necessarily the same' \
                     "as the file's system modification date because it is " \
                     'set before the file is saved.', 'Date',
                     '2005-09-07T15:09:51-07:00')
        tag.metadata = ImageMetadataMock()
        old_value = tag.value
        tag.value = datetime.datetime(2009, 4, 22, 8, 30, 27, tzinfo=FixedOffset())
        self.failIfEqual(tag.value, old_value)
        self.assertEqual(tag.metadata.tags[tag.key], '2009-04-22T08:30:27Z')

    def test_del_value_no_metadata(self):
        tag = XmpTag('Xmp.xmp.ModifyDate', 'ModifyDate', 'Modify Date',
                     'The date and time the resource was last modified. Note:' \
                     ' The value of this property is not necessarily the same' \
                     "as the file's system modification date because it is " \
                     'set before the file is saved.', 'Date',
                     '2005-09-07T15:09:51-07:00')
        del tag.value
        self.failIf(hasattr(tag, 'value'))

    def test_del_value_with_metadata(self):
        tag = XmpTag('Xmp.xmp.ModifyDate', 'ModifyDate', 'Modify Date',
                     'The date and time the resource was last modified. Note:' \
                     ' The value of this property is not necessarily the same' \
                     "as the file's system modification date because it is " \
                     'set before the file is saved.', 'Date',
                     '2005-09-07T15:09:51-07:00')
        tag.metadata = ImageMetadataMock()
        tag.metadata._set_xmp_tag_value(tag.key, tag.to_string())
        self.assertEqual(tag.metadata.tags, {tag.key: '2005-09-07T15:09:51-07:00'})
        del tag.value
        self.failIf(hasattr(tag, 'value'))
        self.failIf(tag.metadata.tags.has_key(tag.key))