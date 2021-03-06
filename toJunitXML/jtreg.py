#!/usr/bin/env python
# encoding: utf-8
"""
jtreg.py

Created by Mahmood Ali on 2009-12-19.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os

from xml.dom.minidom import parse, parseString

def messageFromTR(tr):
    sections = tr.getElementsByTagName("Section")
    str = ""
    for s in sections:
        str += "----------------------------------------------\n"
        str += "== " + s.getAttribute("title") + "\n"
        outputs = s.getElementsByTagName("Output")
        for o in outputs:
            str += o.getAttribute("title") + "\n"
            if (o.firstChild != None):
                str += o.firstChild.data
    return str
     
class JTregReplay(object):
    """docstring for JTregReplay"""
    def __init__(self, report, listener):
        self.report_file = report
        self.listener = listener
        
    def parse(self):
        self.dom = parse(self.report_file)

    def _handle(self, tr):
        name = tr.getAttribute("url")
        status = tr.getAttribute("status")
        message = messageFromTR(tr)
        if (status == "NOT_RUN"):
            self.listener.testIgnored(name, 0, message)
        elif (status == "PASSED"):
            self.listener.testPassed(name, 0, message)
        elif (status == "FAILED"):
            self.listener.testFailed(name, 0, message)
        else:
            print ("UNKNOWN status: " + status)

    def _iterate(self, dom):
        testresults = dom.getElementsByTagName("TestResult")
        i = 0
        for testresult in testresults:
            self._handle(testresult)

    def process(self):
        self.parse()

        self.listener.prepare()
        self._iterate(self.dom)
        self.listener.done()

class Listener(object):
    def prepare(self):
        pass
    
    def testPassed(self, name, time, message):
        pass
        
    def testFailed(self, name, time, message):
        pass
    
    def testErrored(self, name, time, message):
        pass

    def testIgnored(self, name, time, message):
        pass
        
    def done(self):
        pass

def main():
    import junit
    replay = JTregReplay(report = 'sample-jtreg.xml', listener = junit.JunitListener(output = None))
    replay.process()
    
if __name__ == '__main__':
    main()
