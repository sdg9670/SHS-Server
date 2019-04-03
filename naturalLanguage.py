# -*- coding: utf-8 -*-

from konlpy.tag import Mecab


class NaturalLanguage():
    def __init__(self, programs):
        self.programs = programs
        self.db = self.programs['db']
        self.mecab = Mecab()

        self.program_function = {
            1: {1: "알람추가"}
        }

        self.word_freq_vector = {}
        self.word_count = {}
        self.func_count = {}
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
                preq_per[(p, f)] = self.word_freq_vector[(p, f)] / self.func_count[(p, f)] * self.word_count[(p, f)]
        return preq_per;

    def getMostFunc(self, freqPer):
        most_key = ()
        most_value = 0
        for key, value in freqPer.items():
            if value > most_value:
                most_key = key
                most_value = value
        return (most_key, most_value)

    def analysisText(self, text):
        self.loadFunctionData()
        d_text = self.divideText(text)
        self.loadWordData(d_text)
        per = self.getFreqPer()
        pro = self.getMostFunc(per)
        return 'per: %s, pro: %s, d_text: %s' % (per, pro, d_text)
