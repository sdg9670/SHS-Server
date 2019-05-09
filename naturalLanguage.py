# -*- coding: utf-8 -*-

from konlpy.tag import Mecab


class NaturalLanguage():
    def __init__(self, programs):
        self.programs = programs
        self.server = self.programs['server']
        self.db = self.programs['db']
        self.window = self.programs['window']
        self.mecab = Mecab()

        self.text = ''
        self.divide_text = ''
        self.name = ''
        self.ho = 0;
        self.dong = 0;
        self.program_function = {
            1: {1: "알람추가", 2: "알람삭제", 2: "알람수정"},
            2: {1: "창문열기", 2: "창문닫기"},
            3: {1: "커튼열기", 2: "커튼닫기"}
        }

        self.ex_word = [('SN', '-'), ('NNBC', '-'), ('NR', '-'),
                   ('MM', '한'), ('MM', '두'), ('MM', '세'), ('MM', '네'),
                   ('MAG', '내일'), ('MAG', '어제'), ('NNG', '모래'), ('NNG', '아침'), ('NNG', '점심'), ('NNG', '저녁'),
                   ('NNG', '오전'), ('NNG', '오후'), ('NNG', '새벽'), ('NNG', '밤'),
                   ('NNG', '월'), ('NNG', '화'), ('NNG', '수'), ('NNG', '목'), ('NNG', '금'), ('NNG', '토'), ('NNG', '일'),
                   ('NNG', '월요일'), ('NNG', '화요일'), ('NNG', '수요일'), ('NNG', '목요일'), ('NNG', '금요일'), ('NNG', '토요일'),
                   ('NNG', '일요일'), ]

        self.word_freq_vector = {}
        self.word_count = {}
        self.func_count = {}
        self.message = ''
        for p, fs in self.program_function.items():
            for f in fs.keys():
                self.word_freq_vector[(p, f)] = 0
                self.word_count[(p, f)] = 0
                self.func_count[(p, f)] = 0

    def divideText(self, text):
        return self.mecab.pos(text)

    """
    
    단어들의 빈도수의 합 / 실행 횟수 * 단어의 갯수
    
    단어들 정보
    select program, `function`, frequency from word_data where  word = '내일' and part = 'MAG' or word = '맞춰' and part = 'VV+EC';
    word_freq_vector[(program,function)] += frequency
    단어들 갯수
    word_count[(program,function)] ++;
    
    실행 횟수
    select * from function_count
    func_count[(program,function)] = count
    
    """

    def loadFunctionData(self):
        data = self.db.executeQuery('select * from function_count', ())
        for func in data:
            self.func_count[(func[0], func[1])] = func[2]

    def loadWordData(self, d_text):
        string = 'select program, `function`, frequency from word_data where '
        i = 0;
        set_text = set(d_text)
        sql_value = []
        for hts in set_text:
            if i == 0:
                string += 'word = %s and part = %s '
            else:
                string += 'or word = %s and part = %s '
            sql_value.append(hts[0])
            sql_value.append(hts[1])
            i += 1
        data = self.db.executeQuery(string, tuple(sql_value))
        for row in data:
            self.word_freq_vector[(row[0], row[1])] += row[2]
            self.word_count[(row[0], row[1])] += 1

    def getFreqPer(self):
        preq_per = {}
        for p, fs in self.program_function.items():
            for f in fs.keys():
                try:
                    preq_per[(p, f)] = self.word_freq_vector[(p, f)] / self.func_count[(p, f)] * self.word_count[(p, f)]
                except ZeroDivisionError:
                    preq_per[(p, f)] = 0
                    continue
        return preq_per

    def getMostFunc(self, freqPer):
        most_key = None
        most_value = 0
        for key, value in freqPer.items():
            if value > most_value:
                most_key = key
                most_value = value
        if most_key is None:
            return None
        return (most_key, most_value)

    def analysisText(self, text, name, ho, dong):
        self.text = text
        self.loadFunctionData()
        self.divide_text = self.divideText(text)
        self.loadWordData(self.divide_text)

        self.name = name;
        self.ho = ho
        self.dong = dong

        per = self.getFreqPer()
        pro = self.getMostFunc(per)
        if pro is not None:
            print(pro[0][0], pro[1])
            self.runProgram(pro[0][0], pro[0][1])
            self.saveDivideText(pro[0][0], pro[0][1])
        else:
            self.message = '무슨 말씀인지 잘 모르겠습니다.'

    def runProgram(self, pro, func):
        print('getname')
        pro_name = self.getName(pro)
        print(pro_name)
        if self.program_function[pro][func] == "알람추가":
            self.message = '알람을 추가했습니다.'
        elif self.program_function[pro][func] == "알람삭제":
            self.message = '알람을 삭제했습니다.'
        elif self.program_function[pro][func] == "알람수정":
            self.message = '알람을 수정했습니다.'
        elif self.program_function[pro][func] == "창문열기":
            if self.server.checkClientName(pro_name, pro, self.ho, self.dong):
                self.window.openWindow(pro_name)
                self.message = '창문을 열었습니다.'
            else:
                self.message = '존재하지 않는 창문입니다.'
        elif self.program_function[pro][func] == "창문닫기":
            if self.server.checkClientName(pro_name, pro, self.ho, self.dong):
                self.window.closeWindows(pro_name)
                self.message = '창문을 닫았습니다.'
            else:
                self.message = '존재하지 않는 창문입니다.'
        elif self.program_function[pro][func] == "커튼열기":
            self.message = '커튼을 열었습니다.'
        elif self.program_function[pro][func] == "커튼닫기":
            self.message = '커튼을 닫았습니다.'


    def saveDivideText(self, pro, func):
        self.db.updateQuery('insert into `function_count` values(%s, %s, 1) on duplicate key update `count` = `count`+1',
            (pro, func))
        for word, part in self.divide_text:
            if part[0] == 'N' or part[0] == 'V' or part[0] == 'M' or part[0] == 'I':
                for epart, eword in self.ex_word:
                    if not (eword == '-' and epart == part or eword == word and epart == part):
                        self.db.updateQuery('insert into `word_data` values(%s, %s, %s, %s, 1) on duplicate key update `frequency` = `frequency`+1',
                                            (word, part, pro, func))
                        break

    def getMessage(self):
        return self.message

    def getName(self, pro):
        if pro == 2:
            return self.divide_text[self.divide_text.index(('창문', 'NNG')) - 1][0]
        return None
