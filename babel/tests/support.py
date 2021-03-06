# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2011 Edgewall Software
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://babel.edgewall.org/wiki/License.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://babel.edgewall.org/log/.

import doctest
import os
import unittest

from babel import support
from babel.compat import BytesIO, u, b
from babel.messages import Catalog
from babel.messages.mofile import write_mo

class TranslationsTestCase(unittest.TestCase):
    
    def setUp(self):
        # Use a locale which won't fail to run the tests
        os.environ['LANG'] = 'en_US.UTF-8'
        messages1 = [
            ('foo', {'string': 'Voh'}),
            ('foo', {'string': 'VohCTX', 'context': 'foo'}),
            (('foo1', 'foos1'), {'string': ('Voh1', 'Vohs1')}),
            (('foo1', 'foos1'), {'string': ('VohCTX1', 'VohsCTX1'), 'context': 'foo'}),
        ]
        messages2 = [
            ('foo', {'string': 'VohD'}),
            ('foo', {'string': 'VohCTXD', 'context': 'foo'}),
            (('foo1', 'foos1'), {'string': ('VohD1', 'VohsD1')}),
            (('foo1', 'foos1'), {'string': ('VohCTXD1', 'VohsCTXD1'), 'context': 'foo'}),
        ]
        catalog1 = Catalog(locale='en_GB', domain='messages')
        catalog2 = Catalog(locale='en_GB', domain='messages1')
        for ids, kwargs in messages1:
            catalog1.add(ids, **kwargs)            
        for ids, kwargs in messages2:
            catalog2.add(ids, **kwargs)
        catalog1_fp = BytesIO()
        catalog2_fp = BytesIO()
        write_mo(catalog1_fp, catalog1)
        catalog1_fp.seek(0)
        write_mo(catalog2_fp, catalog2)
        catalog2_fp.seek(0)
        translations1 = support.Translations(catalog1_fp)
        translations2 = support.Translations(catalog2_fp, domain='messages1')
        self.translations = translations1.add(translations2, merge=False)

    def assertEqualTypeToo(self, expected, result):
        self.assertEqual(expected, result)
        assert type(expected) == type(result), "instance type's do not " + \
            "match: %r!=%r" % (type(expected), type(result))

    def test_pgettext(self):
        self.assertEqualTypeToo('Voh', self.translations.gettext('foo'))
        self.assertEqualTypeToo(b('VohCTX'), self.translations.pgettext('foo',
                                                                     'foo'))

    def test_upgettext(self):
        self.assertEqualTypeToo(u('Voh'), self.translations.ugettext('foo'))
        self.assertEqualTypeToo(u('VohCTX'), self.translations.upgettext('foo',
                                                                       'foo'))

    def test_lpgettext(self):
        self.assertEqualTypeToo(b('Voh'), self.translations.lgettext('foo'))
        self.assertEqualTypeToo(b('VohCTX'), self.translations.lpgettext('foo',
                                                                      'foo'))

    def test_npgettext(self):
        self.assertEqualTypeToo('Voh1',
                                self.translations.ngettext('foo1', 'foos1', 1))
        self.assertEqualTypeToo('Vohs1',
                                self.translations.ngettext('foo1', 'foos1', 2))
        self.assertEqualTypeToo(b('VohCTX1'),
                                self.translations.npgettext('foo', 'foo1',
                                                            'foos1', 1))
        self.assertEqualTypeToo(b('VohsCTX1'),
                                self.translations.npgettext('foo', 'foo1',
                                                            'foos1', 2))

    def test_unpgettext(self):
        self.assertEqualTypeToo(u('Voh1'),
                                self.translations.ungettext('foo1', 'foos1', 1))
        self.assertEqualTypeToo(u('Vohs1'),
                                self.translations.ungettext('foo1', 'foos1', 2))
        self.assertEqualTypeToo(u('VohCTX1'),
                                self.translations.unpgettext('foo', 'foo1',
                                                             'foos1', 1))
        self.assertEqualTypeToo(u('VohsCTX1'),
                                self.translations.unpgettext('foo', 'foo1',
                                                             'foos1', 2))

    def test_lnpgettext(self):
        self.assertEqualTypeToo(b('Voh1'),
                                self.translations.lngettext('foo1', 'foos1', 1))
        self.assertEqualTypeToo(b('Vohs1'),
                                self.translations.lngettext('foo1', 'foos1', 2))
        self.assertEqualTypeToo(b('VohCTX1'),
                                self.translations.lnpgettext('foo', 'foo1',
                                                             'foos1', 1))
        self.assertEqualTypeToo(b('VohsCTX1'),
                                self.translations.lnpgettext('foo', 'foo1',
                                                             'foos1', 2))

    def test_dpgettext(self):
        self.assertEqualTypeToo(
            'VohD', self.translations.dgettext('messages1', 'foo'))
        self.assertEqualTypeToo(
            b('VohCTXD'), self.translations.dpgettext('messages1', 'foo', 'foo'))

    def test_dupgettext(self):
        self.assertEqualTypeToo(
            u('VohD'), self.translations.dugettext('messages1', 'foo'))
        self.assertEqualTypeToo(
            u('VohCTXD'), self.translations.dupgettext('messages1', 'foo', 'foo'))

    def test_ldpgettext(self):
        self.assertEqualTypeToo(
            b('VohD'), self.translations.ldgettext('messages1', 'foo'))
        self.assertEqualTypeToo(
            b('VohCTXD'), self.translations.ldpgettext('messages1', 'foo', 'foo'))

    def test_dnpgettext(self):
        self.assertEqualTypeToo(
            'VohD1', self.translations.dngettext('messages1', 'foo1', 'foos1', 1))
        self.assertEqualTypeToo(
            'VohsD1', self.translations.dngettext('messages1', 'foo1', 'foos1', 2))
        self.assertEqualTypeToo(
            b('VohCTXD1'), self.translations.dnpgettext('messages1', 'foo', 'foo1',
                                                     'foos1', 1))
        self.assertEqualTypeToo(
            b('VohsCTXD1'), self.translations.dnpgettext('messages1', 'foo', 'foo1',
                                                      'foos1', 2))

    def test_dunpgettext(self):
        self.assertEqualTypeToo(
            u('VohD1'), self.translations.dungettext('messages1', 'foo1', 'foos1', 1))
        self.assertEqualTypeToo(
            u('VohsD1'), self.translations.dungettext('messages1', 'foo1', 'foos1', 2))
        self.assertEqualTypeToo(
            u('VohCTXD1'), self.translations.dunpgettext('messages1', 'foo', 'foo1',
                                                       'foos1', 1))
        self.assertEqualTypeToo(
            u('VohsCTXD1'), self.translations.dunpgettext('messages1', 'foo', 'foo1',
                                                        'foos1', 2))

    def test_ldnpgettext(self):
        self.assertEqualTypeToo(
            b('VohD1'), self.translations.ldngettext('messages1', 'foo1', 'foos1', 1))
        self.assertEqualTypeToo(
            b('VohsD1'), self.translations.ldngettext('messages1', 'foo1', 'foos1', 2))
        self.assertEqualTypeToo(
            b('VohCTXD1'), self.translations.ldnpgettext('messages1', 'foo', 'foo1',
                                                      'foos1', 1))
        self.assertEqualTypeToo(
            b('VohsCTXD1'), self.translations.ldnpgettext('messages1', 'foo', 'foo1',
                                                       'foos1', 2))


class LazyProxyTestCase(unittest.TestCase):
    def test_proxy_caches_result_of_function_call(self):
        self.counter = 0
        def add_one():
            self.counter += 1
            return self.counter
        proxy = support.LazyProxy(add_one)
        self.assertEqual(1, proxy.value)
        self.assertEqual(1, proxy.value)
    
    def test_can_disable_proxy_cache(self):
        self.counter = 0
        def add_one():
            self.counter += 1
            return self.counter
        proxy = support.LazyProxy(add_one, enable_cache=False)
        self.assertEqual(1, proxy.value)
        self.assertEqual(2, proxy.value)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite(support))
    suite.addTest(unittest.makeSuite(TranslationsTestCase, 'test'))
    suite.addTest(unittest.makeSuite(LazyProxyTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
