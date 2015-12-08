#!/usr/bin/python

"""
Copyright (c) 2015. The Koodous Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0
   
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import hashlib
import json
import os
import random
import sys
import unittest

import requests

import koodous

__author__ = "Antonio Sanchez <asanchez@koodous.com>"

"""
Tests for python SDK for Koodous
"""


class TestKoodousSDK(unittest.TestCase):
    def __init__(self, testname, token):
        super(TestKoodousSDK, self).__init__(testname)
        self.koodous = koodous.Koodous(token)
        self.user = None

    def test_utils(self):
        # Test hash256 function
        sha256 = koodous.utils.sha256('tests/sample_test.apk')
        self.assertTrue(
            sha256 == 'e374058ad507072dfa0755371e68a5ef202365c2d3ca4334c3274cdfe01db3bf')

        # Test unpack function
        result = koodous.utils.unpack('tests/sample_test.apk', 'dst_file')
        self.assertTrue(hashlib.sha256(open(
            'dst_file').read()).hexdigest() == 'e374058ad507072dfa0755371e68a5ef202365c2d3ca4334c3274cdfe01db3bf')
        os.remove('dst_file')

    def test_upload(self):
        # With file that already exists (must fail)
        try:
            result = self.koodous.upload('tests/sample_test.apk')
        except Exception, why:
            self.assertTrue(str(why) == "APK already exists")

        # New sample that not exists, I suppose...
        content = open('tests/sample_test.apk', 'rb').read()

        # random sample generation
        randpos = random.randint(3, len(content))
        content = content[:randpos] + chr(0xFF) + chr(0x0A) + content[randpos:]

        with open('sample', 'wb') as fd:
            fd.write(content)

        sha256_hash = koodous.utils.sha256('sample')
        print '\n%s\n' % sha256_hash
        ret = self.koodous.upload('sample')
        os.remove('sample')
        self.assertTrue(ret == sha256_hash)

    def test_download(self):
        # First method, directly to file
        result = self.koodous.download_to_file(
            'ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111',
            'sample')
        sha256_hash = koodous.utils.sha256('sample')

        # The method must return sha256, if return None means download failed
        self.assertTrue(
            result == 'ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111')

        self.assertTrue(
            sha256_hash == 'ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111')
        os.remove('sample')

        # Download to file with download problem
        try:
            result = self.koodous.download_to_file(
                'ace5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111',
                'sample')
            self.assertTrue(False)
        except Exception, why:
            self.assertTrue(str(why) == 'Something was wrong during download')

        # Get the URL and then download:
        url = self.koodous.get_download_url(
            'ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111')
        response = requests.get(url=url)
        sha256_hash = hashlib.sha256(response.content).hexdigest()
        self.assertTrue(
            sha256_hash == 'ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111')

    def test_search(self):
        # With results
        apks = self.koodous.search(
            'whatsapp and package_name:"com.whatsapp" and size:2MB+ and rating:1+')
        self.assertTrue(len(apks) > 0)
        # With no results
        apks = self.koodous.search(
            'whatsapp and package_name:"com.whatsapp" and size:1B- and rating:-5-')
        self.assertTrue(len(apks) == 0)

    def test_analysis(self):
        # With existing hash
        analysis = self.koodous.get_analysis(
            'b1e01902c3e50f3b1181e0267b391dbbd3b69166552cb9ccf08b2a34464a7339')
        self.assertTrue(hashlib.md5(json.dumps(
            analysis)).hexdigest() == '63717947c7e74150f71f5623d5b0318c')
        # With non existing hash
        analysis = self.koodous.get_analysis('abc')
        self.assertTrue(analysis == None)

    def test_strange_analysis(self):
        analysis = self.koodous.get_analysis('79a3bc6da45243355a920082dc67da0febf19379c25c721c43fd6b3f83ff4ef4')

        self.assertTrue(analysis != None)

    def test_request_analysis(self):
        # With good result
        result = self.koodous.analyze(
            'b1e01902c3e50f3b1181e0267b391dbbd3b69166552cb9ccf08b2a34464a7339')
        self.assertTrue(result)
        # With non existing hash, result variable is False
        result = self.koodous.analyze('abc')
        self.assertTrue(result == False)

    def test_comments(self):
        text_posted = self.koodous.post_comment(
            '317de8e1c3fef5130099fe98cdf51793d50669011caf8dd8c9b15714e724a283',
            'test')

        user = self.koodous.my_user()
        username = user.get('username')
        comments = self.koodous.get_comments(
            '317de8e1c3fef5130099fe98cdf51793d50669011caf8dd8c9b15714e724a283')
        self.assertTrue(len(comments) > 0)
        for comment in comments:
            if comment['author']['username'] == username and comment[
                'text'] == 'test':
                ret = self.koodous.delete_comment(comment['id'])
                self.assertTrue(ret)

    def test_get_public_ruleset(self):
        ruleset_id = 685
        created_on = 1436784424
        ruleset = self.koodous.get_public_ruleset(ruleset_id=ruleset_id)

        self.assertEqual(ruleset_id, ruleset['id'])
        self.assertEqual(created_on, ruleset['created_on'])

    def test_get_matches_public_ruleset(self):
        ruleset_id = 709
        apks = self.koodous.get_matches_public_ruleset(ruleset_id=ruleset_id)

        self.assertTrue(len(apks) > 10)

    def test_iter_matches_public_ruleset(self):
        PAGE_LEN = 25
        N_PAGES = 3
        ruleset_id = 836  # >= 151998 matches as of dec 7th, 2015
        all_apks = []
        all_sha256 = []
        results = self.koodous.iter_matches_public_ruleset(
            ruleset_id=ruleset_id)
        i = 0

        for apks in results:
            if i < N_PAGES:
                all_apks.extend(apks)
                all_sha256.extend([a['sha256'] for a in apks])
                self.assertTrue(len(apks) == PAGE_LEN)
            else:
                break
            i += 1

        # no duplicates
        self.assertTrue(
            len(all_sha256) == len(all_apks) == len(list(set(all_sha256))))

        # expected length
        self.assertTrue(len(all_apks) == N_PAGES * PAGE_LEN)


def main():
    try:
        token = sys.argv[1]
    except:
        print "You must provide your Koodous token to pass tests"
        return

    suite = unittest.TestSuite()
    suite.addTest(TestKoodousSDK("test_upload", token))
    suite.addTest(TestKoodousSDK("test_get_matches_public_ruleset", token))
    suite.addTest(TestKoodousSDK("test_iter_matches_public_ruleset", token))
    suite.addTest(TestKoodousSDK("test_search", token))
    suite.addTest(TestKoodousSDK("test_analysis", token))
    suite.addTest(TestKoodousSDK("test_strange_analysis", token))
    suite.addTest(TestKoodousSDK("test_get_public_ruleset", token))
    suite.addTest(TestKoodousSDK("test_request_analysis", token))
    suite.addTest(TestKoodousSDK("test_download", token))
    suite.addTest(TestKoodousSDK("test_comments", token))
    suite.addTest(TestKoodousSDK("test_utils", token))

    unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    main()
