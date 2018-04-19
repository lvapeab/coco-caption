#!/usr/bin/env python

# Python wrapper for METEOR implementation, by Xinlei Chen
# Acknowledge Michael Denkowski for the generous discussion and help 
import os
import subprocess
import threading
import time
import sys
# Assumes meteor-1.5.jar is in the same directory as meteor.py.  Change as needed.
METEOR_JAR = 'meteor-1.5.jar'


class Meteor:
    def __init__(self, language='en'):
        d = dict(os.environ.copy())
        d['LANG'] = 'C'
        self.meteor_cmd = ['java', '-jar', '-Xmx2G', METEOR_JAR, '-', '-', '-stdio', '-l', language, '-norm']
        self.meteor_p = subprocess.Popen(self.meteor_cmd, cwd=os.path.dirname(os.path.abspath(__file__)),
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         env=d)
        # Used to guarantee thread safety
        self.lock = threading.Lock()

    def compute_score(self, gts, res):
        assert(gts.keys() == res.keys())
        imgIds = gts.keys()
        scores = []
        eval_line = 'EVAL'
        self.lock.acquire()
        for i in imgIds:
            assert(len(res[i]) == 1)
            if sys.version_info.major == 2:
                for j in range(len(gts[i])):
                    # Convert to UTF-8 if necessary
                    if type(gts[i][j]) == str:
                        gts[i][j] = gts[i][j].decode('utf-8')
            stat = self._stat(res[i][0], gts[i])
            eval_line += u' ||| {}'.format(stat)

        if sys.version_info.major == 2:
            self.meteor_p.stdin.write(u'{}\n'.format(eval_line))

        else:
            self.meteor_p.stdin.write(u'{}\n'.format(eval_line).encode())
        time.sleep(1)
        for i in range(0, len(imgIds)):
            scores.append(float(self.meteor_p.stdout.readline().strip()))
        score = float(self.meteor_p.stdout.readline().strip())
        self.lock.release()
        self.meteor_p.kill()
        return score, scores

    def method(self):
        return "METEOR"

    def _stat(self, hypothesis_str, reference_list):
        # SCORE ||| reference 1 words ||| reference n words ||| hypothesis words
        hypothesis_str = hypothesis_str.replace(u'|||', u'').replace(u'  ', u' ')
        score_line = u' ||| '.join(('SCORE', ' ||| '.join(reference_list), hypothesis_str))
        if sys.version_info.major == 2:
            self.meteor_p.stdin.write('{}\n'.format(score_line.encode('utf-8')))
            return self.meteor_p.stdout.readline().strip()

        else:
            self.meteor_p.stdin.write('{}\n'.format(score_line).encode())
            self.meteor_p.stdin.flush()
            return self.meteor_p.stdout.readline().decode().strip()
    def _score(self, hypothesis_str, reference_list):
        self.lock.acquire()
        # SCORE ||| reference 1 words ||| reference n words ||| hypothesis words
        hypothesis_str = hypothesis_str.replace(u'|||', u'').replace(u'  ', u' ')
        score_line = u' ||| '.join((u'SCORE', u' ||| '.join(reference_list), hypothesis_str))
        self.meteor_p.stdin.write(u'{}\n'.format(score_line))
        stats = self.meteor_p.stdout.readline().strip()
        eval_line = u'EVAL ||| {}'.format(stats)

        # EVAL ||| stats
        self.meteor_p.stdin.write(u'{}\n'.format(eval_line))
        score = float(self.meteor_p.stdout.readline().strip())
        # bug fix: there are two values returned by the jar file, one average, and one all, so do it twice
        # thanks for Andrej for pointing this out
        score = float(self.meteor_p.stdout.readline().strip())
        self.lock.release()
        return score

    def __del__(self):
        self.lock.acquire()
        self.meteor_p.stdin.close()
        self.meteor_p.kill()
        self.meteor_p.wait()
        self.lock.release()
