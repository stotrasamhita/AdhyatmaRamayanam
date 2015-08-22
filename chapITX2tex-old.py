#!/usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import re

import transliterator


def i2d(text):
    newtext = text.strip('|')
    # print(newtext,file=sys.stderr)
    if newtext[-1] == 'M':
        newtext = newtext[:-1] + 'm'
    text = newtext + '|'*(len(text)-len(newtext))

    text_parts = text.split()
    out_text_parts = []
    for t in text_parts:
        try:
            out_text = transliterator.transliterate(t, 'itrans', 'devanagari')
        except:
            e = sys.exc_info()[0]
            sys.stderr.write(
                'Error transliterating the string "%s"...\n' % (t))
            out_text = '##%s##' % t
        out_text_parts.append(out_text)

    return ' '.join(out_text_parts)

chapFile = open(sys.argv[1])
# chapFile = open('adhyaatmaRamBal.itx.txt')

sargaCount = 0
twoLine = False
fourLine = False
iti = False
for line in chapFile.readlines():
    line = line.strip('\n')

    if line == '':
        continue

    if line[-5:] == 'vAcha':
        print('\n\\textbf{%s}' % i2d(line.strip()))
        continue

    if twoLine:
        if re.match('.*[0-9]', line) is not None:
            twoLine = False
            lineData = line.split()
            # print(lineData, file=sys.stderr)
            shlokaData = i2d(' '.join(lineData[:-2]))
            shlokaNum = int(lineData[-1].strip('|'))
            print('{%s} %%%d-%d' % (shlokaData, sargaCount, shlokaNum))
        else:
            print('{%s}' % i2d(line.strip()))
    elif fourLine:
        if re.match('.*[0-9]', line) is not None:
            fourLine = False
            lineData = line.split()
            shlokaData = i2d(' '.join(lineData[:-2]))
            shlokaNum = int(lineData[-1].strip('|'))
            print('{%s} %%%d-%d' % (shlokaData, sargaCount, shlokaNum))
        else:
            print('{%s}' % i2d(line.strip('|')))
    elif iti:
        if line[1:4] == 'iti':
            print('}\n%%%%%%%%%%%%%%%%%%%%\n')
            iti = False
        else:
            print('%s' % i2d(line.strip()))
    elif line[:2] == '||' and line[-2:] == '||':
        print('%s' % i2d(line))
    elif line[-5:] == 'vAcha':
        print('\n\\textbf{%s}' % i2d(line.strip()))
    elif line[:8] == '\chapter':
        line = re.sub(r'^.*\{', '', line)
        line = re.sub(r'}', '', line)
        print('\n\n\chapt{%s}' % i2d(line.strip(' |')))
    elif line[:8] == '\section':
        line = re.sub(r'^.*\{', '', line)
        line = re.sub(r'}', '', line)
        print('\n\n\sect{%s}' % i2d(line.strip(' |')))
        sargaCount += 1
    elif line[-2:] == ' |':
        print('\n\\twolineshloka')
        print('{%s}' % i2d(line.strip('| ')))
        twoLine = True
    elif line[:8] == 'iti shrI':
        iti = True
        print('\n{%s' % i2d(line.strip()))
        # We have the end of the verse
    elif re.match('.*[0-9]', line) is not None:
        # We have a one line shloka
        print('{%s}\n\\refstepcounter{shlokacount}\n' % i2d(line.strip()))
    else:
        # We have a four line shloka
        print('\n\\fourlineindentedshloka')
        print('{%s}' % i2d(line.strip()))
        fourLine = True
