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

import unittest
import json
import sys
import hashlib
import requests
import os

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
        #Test hash256 function
        sha256 = koodous.utils.sha256('tests/sample_test.apk')
        self.assertTrue(sha256 == 'e374058ad507072dfa0755371e68a5ef202365c2d3ca4334c3274cdfe01db3bf')

    
        #Test unpack function
        result = koodous.utils.unpack('tests/sample_test.apk', 'dst_file')
        self.assertTrue(hashlib.sha256(open('sample').read()).hexdigest() == 'ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111')
        os.remove('dst_file')

    def test_upload(self):
        def create_random_apk():
            pass
        #self.koodous.upload(filepath)
        #TODO
        return
        
    def test_download(self):
        #First method, directly to file
        result = self.koodous.download_to_file('ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111', 'sample')
        sha256_hash = hashlib.sha256(open('sample').read()).hexdigest()
        #The method must return sha256, if return None means download failed
        self.assertTrue(result == 'ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111')

        self.assertTrue(sha256_hash == 'ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111')
        os.remove('sample')

        #Download to file with download problem
        try:
            result = self.koodous.download_to_file('ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111', 'sample')
            self.assertTrue(False)
        except:
            pass

        #Get the URL and then download:
        url = self.koodous.get_download_url('ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111')
        response = requests.get(url=url)
        sha256_hash = hashlib.sha256(response.content).hexdigest()
        self.assertTrue(sha256_hash == 'ce5db3ec259792f80680ad2217af240d10fb4e1939226087d835cf4b2b837111')


    def test_search(self):
        #With results
        apks = self.koodous.search('whatsapp and package_name:"com.whatsapp" and size:2MB+ and rating:1+')
        self.assertTrue(len(apks) > 0)
        #With no results
        apks = self.koodous.search('whatsapp and package_name:"com.whatsapp" and size:1B- and rating:-5-')
        self.assertTrue(len(apks) == 0)

    def test_analysis(self):
        #With existing hash
        analysis = self.koodous.get_analysis('b1e01902c3e50f3b1181e0267b391dbbd3b69166552cb9ccf08b2a34464a7339')
        self.assertTrue(hashlib.md5(json.dumps(analysis)).hexdigest() == '719a027b3462b48929463dc65115f810')
        #With non existing hash
        analysis = self.koodous.get_analysis('abc')
        self.assertTrue(analysis == None)


    def test_request_analysis(self):
        #With good result
        result = self.koodous.analyze('b1e01902c3e50f3b1181e0267b391dbbd3b69166552cb9ccf08b2a34464a7339')
        self.assertTrue(result)
        #With non existing hash, result variable is False     
        result = self.koodous.analyze('abc')
        self.assertTrue(result == False)


    def test_comments(self):
        text_posted = self.koodous.post_comment('317de8e1c3fef5130099fe98cdf51793d50669011caf8dd8c9b15714e724a283', 'test')
        
        user = self.koodous.my_user()
        username = user.get('username')
        comments = self.koodous.get_comments('317de8e1c3fef5130099fe98cdf51793d50669011caf8dd8c9b15714e724a283')
        self.assertTrue(len(comments) > 0)
        for comment in comments:
            if comment['author']['username'] == username and comment['text'] == 'test':
                ret = self.koodous.delete_comment(comment['id'])
                self.assertTrue(ret)

def main():
    try:
        token = sys.argv[1]
    except:
        print "You must provide your token to use pass tests"
        return

    suite = unittest.TestSuite()
    #suite.addTest(TestKoodousSDK("test_upload", token))
    suite.addTest(TestKoodousSDK("test_search", token))
    suite.addTest(TestKoodousSDK("test_analysis", token))
    suite.addTest(TestKoodousSDK("test_request_analysis", token))
    suite.addTest(TestKoodousSDK("test_download", token))
    suite.addTest(TestKoodousSDK("test_comments", token))
    suite.addTest(TestKoodousSDK("test_utils", token))

    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    main()
