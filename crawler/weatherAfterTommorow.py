from bs4 import BeautifulSoup

def weatherAfterTommorow(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    div = bsObj.find("div", {"class": "main_info"})
    if div is None:
        return None
    ondo = div.find("p", {"class": "info_temperature"})
    weather = div.find("ul", {"class": "info_list"})
    week = weather.findAll("li", {"class": ""})
    aftertomorrowAll = {}
    # 오늘
    # 두번째칸-1
    todayTemp = bsObj.findAll("ul", {"class": "list_area"})


    weekWeather = bsObj.findAll("ul", {"class": "list_area _pageList"})
    weekWeather1 = weekWeather[0].findAll("li", {"class": "date_info today"})
    weekWeather2 = weekWeather[1].findAll("li", {"class": "date_info today"})

    area = bsObj.find("div", {"class": "select_box"})
    areaA = area.find("em")
    # 오늘 끝

    # 내일 시작
    # 내일 - 첫번째칸
    tomorrow = bsObj.findAll("div", {"class": "main_info morning_box"})

    # 모레 시작
    # 내일 - 첫번째칸
    aftertomorrowMorningondo = tomorrow[2].find("p", {"class": "info_temperature"})
    aftertomorrowMorningWeath = tomorrow[2].find("ul", {"class": "info_list"})
    aftertomorrowMorningWeath_1 = aftertomorrowMorningWeath.findAll("li", {"class": ""})
    aftertomorrowAfternoonondo = tomorrow[3].find("p", {"class", "info_temperature"})
    aftertomorrowAfternoonWeath = tomorrow[3].find("ul", {"class", "info_list"})
    aftertomorrowAfternoonWeath_1 = aftertomorrowAfternoonWeath.findAll("li", {"class": ""})
    # 내일 - 두번째칸1

    aftertomorrowTimeTemp1 = todayTemp[8].findAll("li")
    # 모레 끝

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


    # 모레 시작
    AftertomorrowWeather = {"지역":areaA.text,"오전날씨": aftertomorrowMorningWeath_1[0].text, "오전온도": aftertomorrowMorningondo.text,
                            "오전미세먼지": aftertomorrowMorningWeath_1[1].text, "오후온도": aftertomorrowAfternoonondo.text,
                            "오후날씨": aftertomorrowAfternoonWeath_1[0].text,
                            "오후미세먼지": aftertomorrowAfternoonWeath_1[1].text}
    aftertomorrowWeatherOndo = []
    for i in range(0, 8):
        aftertomorrowWeatherOndo.append(aftertomorrowTimeTemp1[i].text.split())

    aftertomorrowWeatherSum = {}
    aftertomorrowWeatherSum = {0: {"시간": aftertomorrowWeatherOndo[0][6], "온도": aftertomorrowWeatherOndo[0][2],
               "날씨": aftertomorrowWeatherOndo[0][4]},1: {"시간": aftertomorrowWeatherOndo[1][6], "온도": aftertomorrowWeatherOndo[1][2],
                "날씨": aftertomorrowWeatherOndo[1][4]},2: {"시간": aftertomorrowWeatherOndo[2][6], "온도": aftertomorrowWeatherOndo[2][2],
                "날씨": aftertomorrowWeatherOndo[2][4]},3: {"시간": aftertomorrowWeatherOndo[3][6], "온도": aftertomorrowWeatherOndo[3][2],
                "날씨": aftertomorrowWeatherOndo[3][4]},4: {"시간": aftertomorrowWeatherOndo[4][6], "온도": aftertomorrowWeatherOndo[4][2],
                "날씨": aftertomorrowWeatherOndo[4][4]},5: {"시간": aftertomorrowWeatherOndo[5][6], "온도": aftertomorrowWeatherOndo[5][2],
                "날씨": aftertomorrowWeatherOndo[5][4]},6: {"시간": aftertomorrowWeatherOndo[6][6], "온도": aftertomorrowWeatherOndo[6][2],
                "날씨": aftertomorrowWeatherOndo[6][4]},7: {"시간": aftertomorrowWeatherOndo[7][6], "온도": aftertomorrowWeatherOndo[7][2],
                "날씨": aftertomorrowWeatherOndo[7][4]}}

    aftertomorrowAll = {"날씨": AftertomorrowWeather, "시간별날씨": aftertomorrowWeatherSum, "주간날씨": weekWeatherSum}
    return aftertomorrowAll