# -*- coding: utf-8 -*-

import os
import naturalLanguage
from konlpy.tag import Mecab
import  databaseManager

mecab = Mecab()
db = databaseManager.DatabaseManager('localhost', 'root', '!Dasom0129', 'shs')

ex_word = [('SN', '-'), ('NNBC', '-'), ('NR', '-'),
                ('MM', '한'), ('MM', '두'), ('MM', '세'), ('MM', '네'),
                ('MAG', '내일'), ('MAG', '어제'), ('NNG', '모래'), ('NNG', '아침'), ('NNG', '점심'), ('NNG', '저녁'),
                ('NNG', '오전'), ('NNG', '오후'), ('NNG', '새벽'), ('NNG', '밤'),
                ('NNG', '월'), ('NNG', '화'), ('NNG', '수'), ('NNG', '목'), ('NNG', '금'), ('NNG', '토'), ('NNG', '일'),
                ('NNG', '월요일'), ('NNG', '화요일'), ('NNG', '수요일'), ('NNG', '목요일'), ('NNG', '금요일'), ('NNG', '토요일'), ('NNG', '일요일'),]

program_function = {
    1: {1: "알람추가", 2: "알람삭제", 3: "알람수정"},
    2: {1: "창문열기", 2: "창문닫기"},
    3: {1: "커튼열기", 2: "커튼닫기"}
}

def saveDivideText(pro, func):
    db.updateQuery('insert into `function_count` values(%s, %s, 1) on duplicate key update `count` = `count`+1', (pro, func))
    for word, part in divide_text:
        if part[0] == 'N' or part[0] == 'V' or part[0] == 'M' or part[0] == 'I':
            for epart, eword in ex_word:
                if not (eword == '-' and epart == part or eword == word and epart == part):
                    string = 'insert into `word_data` values(%s, %s, %s, %s, 1) on duplicate key update `frequency` = `frequency`+1'
                    db.updateQuery(string, (word, part, pro, func))
                    break




file_list = os.listdir('WordData')
for file in file_list:
    f = open('WordData/' + file, 'r')
    split_str = file.split('.')
    for pro_key in program_function.keys():
        for func_key in range(1, len(program_function.values())):
            if split_str[0] == program_function[pro_key][func_key]:
                for line in f.readlines():
                    divide_text = mecab.pos(line)
                    saveDivideText(pro_key, func_key)


