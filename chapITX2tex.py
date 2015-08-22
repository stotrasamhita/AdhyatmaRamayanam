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

if __name__ == '__main__':
    chapFile = open(sys.argv[1])
    # chapFile = open('adhyaatmaRamBal.itx.txt')

    sargaCount = 0
    twoThreeLine = False
    fourLine = False
    outputShloka = ''
    nLines = 0
    iti = False
    for line in chapFile.readlines():
        line = line.strip('\n')

        if line == '':
            continue

        if line[-5:] == 'vAcha':
            print('\n\\textbf{%s}' % i2d(line.strip()))
            continue

        if twoThreeLine:
            if re.match('.*\|\|', line) is not None:
                if re.match ('.*[0-9]', line) is None:
                    #we have an un-numbered shloka
                    twoThreeLine = False
                    nLines += 1

                    if nLines == 2:
                        print ('\n\\twolineshloka*')
                    elif nLines == 3:
                        print ('\n\\threelineshloka*')
                    print (outputShloka)
                    print ('{%s}' % i2d(line.strip('| ')))
                    outputShloka = ''
                    nLines = 0
                else:
                    #We have a number in this line
                    twoThreeLine = False
                    nLines += 1
                    
                    lineData = line.split()
                    shlokaData = i2d(' '.join(lineData[:-2]))
                    shlokaNum = int(lineData[-1].strip('|'))
                    
                    if nLines == 2:
                    	print ('\n\\twolineshloka')
                    elif nLines == 3:
                    	print ('\n\\threelineshloka')
                    print (outputShloka)
                    print('{%s} %%%d-%d' % (shlokaData, sargaCount, shlokaNum))
                    outputShloka = ''
                    nLines = 0
            else:
                nLines += 1
                outputShloka += '\n{%s}' % i2d(line.strip('| '))
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
        elif line[-5:] == 'vAcha' or line[-5:] == 'UchuH':
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
            outputShloka += '{%s}' % i2d(line.strip('| '))
            twoThreeLine = True
            nLines += 1
        elif line[:8] == 'iti shrI':
            iti = True
            print('\n{%s' % i2d('..'+line.strip()))
            # We have the end of the verse
        elif re.match('.*[0-9]', line) is not None:
            # We have a one line shloka
            # Need to remove the space before the number using an re.sub
            # line = re.sub(r' \|\| ','||',line)
            lineData = line.split()
            shlokaNum = int(lineData[-1].strip('|'))
            shlokaData = i2d(' '.join(lineData[:-2])) + i2d('..'+str(shlokaNum)+'..')
            # print(i2d(line),file=sys.stderr)
            # print('\n{%s}\n\\refstepcounter{shlokacount}\n' % i2d(line.strip()))
            print('\n{%s} %%%d-%d\n\\refstepcounter{shlokacount}\n' % (shlokaData, sargaCount, shlokaNum))
            # print('\n{%s} %%%d-%d\n\\refstepcounter{shlokacount}\n' % (shlokaData, sargaCount, shlokaNum), file=sys.stderr)
        else:
            # We have a four line shloka
            print('\n\\fourlineindentedshloka')
            print('{%s}' % i2d(line.strip()))
            fourLine = True
