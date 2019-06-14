from bs4 import BeautifulSoup

def weatherTomorrow(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    div = bsObj.find("div", {"class": "main_info"})
    if div is None:
        return None
    ondo = div.find("p", {"class": "info_temperature"})
    weather = div.find("ul", {"class": "info_list"})
    week = weather.findAll("li", {"class": ""})
    tomorrowAll = {}
    # 오늘
    # 두번째칸-1
    todayTemp = bsObj.findAll("ul", {"class": "list_area"})


    weekWeather = bsObj.findAll("ul", {"class": "list_area _pageList"})
    weekWeather1 = weekWeather[0].findAll("li", {"class": "date_info today"})
    weekWeather2 = weekWeather[1].findAll("li", {"class": "date_info today"})

    area = bsObj.find("div", {"class": "select_box"})
    areaA = area.find("em")


    # 내일 시작
    # 내일 - 첫번째칸
    tomorrow = bsObj.findAll("div", {"class": "main_info morning_box"})
    tomorrowMorning = tomorrow[0].find("p", {"class": "info_temperature"})
    tomorrowMorningWeath = tomorrow[0].find("ul", {"class": "info_list"})
    tomorrowAfternoon = tomorrow[1].find("p", {"class", "info_temperature"})
    tomorrowAfternoonWeath = tomorrow[1].find("ul", {"class", "info_list"})

    # 내일 - 두번째칸1
    tomorrowTimeTemp = todayTemp[4].find("li", {"class": "now"})
    tomorrowTimeTemp1 = todayTemp[4].findAll("li", {"class": ""})
    tomorrowTimeTempLast = todayTemp[4].find("li", {"class": "last"})
    # 내일 끝


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


    # 내일 시작
    tomorrowTimeTempReal = []
    tomorrowTimeTempReal.append(tomorrowTimeTemp.text.split())
    for i in range(0, 6):
        tomorrowTimeTempReal.append(tomorrowTimeTemp1[i].text.split())
    tomorrowTimeTempReal.append(tomorrowTimeTempLast.text.split())

    tomorrowWeatherSum = {}
    tomorrowWeatherSum = {
        0: {"시간": tomorrowTimeTempReal[0][6], "온도": tomorrowTimeTempReal[0][2], "날씨": tomorrowTimeTempReal[0][4]},
        1: {"시간": tomorrowTimeTempReal[1][6], "온도": tomorrowTimeTempReal[1][2], "날씨": tomorrowTimeTempReal[1][4]},
        2: {"시간": tomorrowTimeTempReal[2][6], "온도": tomorrowTimeTempReal[2][2], "날씨": tomorrowTimeTempReal[2][4]},
        3: {"시간": tomorrowTimeTempReal[3][6], "온도": tomorrowTimeTempReal[3][2], "날씨": tomorrowTimeTempReal[3][4]},
        4: {"시간": tomorrowTimeTempReal[4][6], "온도": tomorrowTimeTempReal[4][2], "날씨": tomorrowTimeTempReal[4][4]},
        5: {"시간": tomorrowTimeTempReal[5][6], "온도": tomorrowTimeTempReal[5][2], "날씨": tomorrowTimeTempReal[5][4]},
        6: {"시간": tomorrowTimeTempReal[6][6], "온도": tomorrowTimeTempReal[6][2], "날씨": tomorrowTimeTempReal[6][4]},
        7: {"시간": tomorrowTimeTempReal[7][6], "온도": tomorrowTimeTempReal[7][2], "날씨": tomorrowTimeTempReal[7][4]}}
    print(tomorrowAfternoonWeath.text)
    print(tomorrowMorningWeath.text)
    tomorrowM = tomorrowMorningWeath.text.split("    ")
    tomorrowA = tomorrowAfternoonWeath.text.split("    ")
    tomorrowWeather = {"지역":areaA.text,"오전날씨": tomorrowM[0], "오전온도": tomorrowMorning.text, "오전미세먼지": tomorrowM[1].replace("미세먼지 ",""), "오후날씨": tomorrowA[0],
                       "오후온도": tomorrowAfternoon.text, "오후미세먼지": tomorrowA[1].replace("미세먼지 ","")}

    # 내일 끝
    tomorrowAll={"날씨":tomorrowWeather,"시간별날씨":tomorrowWeatherSum,"주간날씨":weekWeatherSum}
    return tomorrowAll