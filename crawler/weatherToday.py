from bs4 import BeautifulSoup

def weatherToday(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    div = bsObj.find("div", {"class": "main_info"})
    if div is None:
        return None
    ondo = div.find("p", {"class": "info_temperature"})
    weather = div.find("ul", {"class": "info_list"})
    week = weather.findAll("li", {"class": ""})
    todayAll = {}
    # 오늘
    # 두번째칸-1
    todayTemp = bsObj.findAll("ul", {"class": "list_area"})
    todayTemp1 = todayTemp[0].findAll("li", {"class": "on"})
    todayTemp2 = todayTemp[0].findAll("li", {"class": ""})
    todayTemp3 = todayTemp[0].find("li", {"class": "last"})

    # 세번째칸
    munji = bsObj.find("dl", {"class": "indicator"})
    mise = munji.text.split()

    weekWeather = bsObj.findAll("ul", {"class": "list_area _pageList"})
    weekWeather1 = weekWeather[0].findAll("li", {"class": "date_info today"})
    weekWeather2 = weekWeather[1].findAll("li", {"class": "date_info today"})

    area = bsObj.find("div", {"class": "select_box"})
    areaA = area.find("em")
    # 오늘 끝


    # 오늘 시작
    weekWeather1_1 = []
    weekWeather2_1 = []
    weekWeatherSum = {}
    weekWeatherOndo = []
    for i in range(0, 5):
        weekWeather1_1.append(weekWeather1[i].text.split())

        weekWeatherOndo.append(weekWeather1_1[i][8].split('/'))
    for i in range(0, 5):
        weekWeather2_1.append(weekWeather2[i].text.split())
        weekWeatherOndo.append(weekWeather2_1[i][8].split('/'))

    weekWeatherSum = {0: {"요일": weekWeather1_1[0][0], "날짜": weekWeather1_1[0][1], "오전강수": weekWeather1_1[0][3],
                          "오후강수": weekWeather1_1[0][5], "최고기온": weekWeatherOndo[0][0], "최저기온": weekWeatherOndo[0][1]},
                      1: {"요일": weekWeather1_1[1][0], "날짜": weekWeather1_1[1][1], "오전강수": weekWeather1_1[1][3],
                          "오후강수": weekWeather1_1[1][5], "최고기온": weekWeatherOndo[1][0], "최저기온": weekWeatherOndo[1][1]},
                      2: {"요일": weekWeather1_1[2][0], "날짜": weekWeather1_1[2][1], "오전강수": weekWeather1_1[2][3],
                          "오후강수": weekWeather1_1[2][5], "최고기온": weekWeatherOndo[2][0], "최저기온": weekWeatherOndo[2][1]},
                      3: {"요일": weekWeather1_1[3][0], "날짜": weekWeather1_1[3][1], "오전강수": weekWeather1_1[3][3],
                          "오후강수": weekWeather1_1[3][5], "최고기온": weekWeatherOndo[3][0], "최저기온": weekWeatherOndo[3][1]},
                      4: {"요일": weekWeather1_1[4][0], "날짜": weekWeather1_1[4][1], "오전강수": weekWeather1_1[4][3],
                          "오후강수": weekWeather1_1[4][5], "최고기온": weekWeatherOndo[4][0], "최저기온": weekWeatherOndo[4][1]},
                      5: {"요일": weekWeather2_1[0][0], "날짜": weekWeather2_1[0][1], "오전강수": weekWeather2_1[0][3],
                          "오후강수": weekWeather2_1[0][5], "최고기온": weekWeatherOndo[5][0], "최저기온": weekWeatherOndo[5][1]},
                      6: {"요일": weekWeather2_1[1][0], "날짜": weekWeather2_1[1][1], "오전강수": weekWeather2_1[1][3],
                          "오후강수": weekWeather2_1[1][5], "최고기온": weekWeatherOndo[6][0], "최저기온": weekWeatherOndo[6][1]},
                      7: {"요일": weekWeather2_1[2][0], "날짜": weekWeather2_1[2][1], "오전강수": weekWeather2_1[2][3],
                          "오후강수": weekWeather2_1[2][5], "최고기온": weekWeatherOndo[7][0], "최저기온": weekWeatherOndo[7][1]},
                      8: {"요일": weekWeather2_1[3][0], "날짜": weekWeather2_1[3][1], "오전강수": weekWeather2_1[3][3],
                          "오후강수": weekWeather2_1[3][5], "최고기온": weekWeatherOndo[8][0], "최저기온": weekWeatherOndo[8][1]},
                      9: {"요일": weekWeather2_1[4][0], "날짜": weekWeather2_1[4][1], "오전강수": weekWeather2_1[4][3],
                          "오후강수": weekWeather2_1[4][5], "최고기온": weekWeatherOndo[9][0], "최저기온": weekWeatherOndo[9][1]}
                      }

    todayFirstWeather = weather.text.split()
    todayLowOndo = todayFirstWeather[4].split('/')
    todayTempEnd = todayTemp[0].text.split()
    todayTempSum = {}

    num=0
    for i in range(0, 8):
        # 2,9,16,
        todayTempSum[i] = {}
        if todayTempEnd[6 + i * 7]=="내일":
            num=1
            todayTempSum[i]["시간"] = todayTempEnd[7 + i * 7]
            todayTempSum[i]["온도"] = todayTempEnd[2 + i * 7]
            todayTempSum[i]["날씨"] = todayTempEnd[4 + i * 7]
        elif num==1:
            todayTempSum[i]["시간"] = todayTempEnd[7 + i * 7]
            todayTempSum[i]["온도"] = todayTempEnd[3 + i * 7]
            todayTempSum[i]["날씨"] = todayTempEnd[5 + i * 7]
        else:
            todayTempSum[i]["시간"] = todayTempEnd[6 + i * 7]
            todayTempSum[i]["온도"] = todayTempEnd[2 + i * 7]
            todayTempSum[i]["날씨"] = todayTempEnd[4 + i * 7]


    todayWeather = {"지역": areaA.text, "날씨": week[0].text, "온도": ondo.text, "최저기온": todayLowOndo[0],
                    "최고기온": todayLowOndo[1], "체감온도": todayFirstWeather[6], "미세먼지": mise[1],
                    "초미세먼지": mise[3], "오존지수": mise[5]}

    # 오늘 끝

    todayAll={"날씨":todayWeather,"시간별날씨":todayTempSum,"주간날씨":weekWeatherSum}
    return todayAll