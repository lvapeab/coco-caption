#!/usr/bin/env python

# Python wrapper for TER implementation, by Alvaro Peris.
# Based on the Meteor implementation from PycocoEvalCap

import os
import subprocess
import threading

# Assumes tercom.7.25 and tercom.7.25.jar is in the same directory as ter.py.  Change as needed.

TER_JAR = 'tercom.7.25'


class Ter:
    def __init__(self, additional_flags=''):
        self.d = dict(os.environ.copy())
        self.d['LANG'] = 'C'
        self.ter_cmd = "bash " + TER_JAR + " -r /tmp/aux.ref -h /tmp/aux.hyp " \
                       + additional_flags + "| grep TER | awk '{print $3}'"
        # Used to guarantee thread safety
        self.lock = threading.Lock()

    def compute_score(self, gts, res):
        assert (gts.keys() == res.keys())
        imgIds = gts.keys()
        self.lock.acquire()
        gts_ter = ''
        res_ter = ''
        warn = False
        for i in imgIds:
            assert (len(res[i]) == 1)
            if len(gts[i]) > 1:
                warn = True
            gts_ter += gts[i][0] + '\t(sentence%d)\n' % i
            res_ter += res[i][0] + '\t(sentence%d)\n' % i
            with open('/tmp/aux.ref', 'w') as f:
                f.write(gts_ter)
            with open('/tmp/aux.hyp', 'w') as f:
                f.write(res_ter)
        if warn:
            print "Warning! Multi-reference TER unimplemented!"
        self.ter_p = subprocess.Popen(self.ter_cmd, cwd=os.path.dirname(os.path.abspath(__file__)),
                                      stdout=subprocess.PIPE, shell=True, env=self.d)
        score = self.ter_p.stdout.read()
        self.lock.release()
        self.ter_p.kill()
        return float(score), None

    def method(self):
        return "TER"

    def __del__(self):
        self.lock.acquire()
        self.ter_p.kill()
        self.ter_p.wait()
        self.lock.release()
