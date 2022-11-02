from msilib.schema import tables
import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
import folium



def crawling_food_store_name(url:str):
    url = url
    res = req.get(url)
    soup = bs(res.text, 'html.parser')

    tds = soup.find_all('td')

    sikyung_mu = []

    for td in tds:
        td_text = td.get_text(strip=True)
        sikyung_mu.append(td_text)

    table_len = int(len(sikyung_mu) / 5)

    sort_table = []

    for i in range(table_len):
        name = sikyung_mu[i*5]
        menu = sikyung_mu[(i*5)+1]
        addr1 = sikyung_mu[(i*5)+2]
        addr2 = sikyung_mu[(i*5)+3]
        addr3 = sikyung_mu[(i*5)+4]
        table = [name, menu, addr1, addr2, addr3]
        sort_table.append(table)

    df = pd.DataFrame(sort_table[1:len(sort_table)-1], columns=sort_table[0])

    return df


def search_kakao_address(address: str):
    searching = address

    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)

    rest_api_key = '6a685d8c81c849264dec05b1cbc4094f'

    header = {'Authorization': 'KakaoAK ' + rest_api_key}

    places = req.get(url, headers=header).json()['documents']
    
    return places


def make_map(db, col=None, category_name=None):
    
    
    
    m = folium.Map(location=[35.809747, 127.092337], zoom_start=13)

    if col == None and category_name == None:
        for i in range(len(db)):
            iframe = folium.IFrame('가게명:' + str(db.iloc[i]['name']) + '<br>' +
                                   '출현방송:' + str(db.iloc[i]['category']) + '<br>' +
                                   '주소:' + str(db.iloc[i]['addr3']) + '<br>' +
                                   '메뉴:' + str(db.iloc[i]['menu'])
                                   )
            popup = folium.Popup(iframe, min_width=20, max_width=100)
            folium.Marker([db.iloc[i]['y_code'], db.iloc[i]['x_code']], popup=popup).add_to(m)

    else:
        map_db = db[db[col] == category_name]
        for i in range(len(map_db)):
            iframe = folium.IFrame('가게명:' + str(map_db.iloc[i]['name']) + '<br>' +
                                   '출현방송:' + str(map_db.iloc[i]['category']) + '<br>' +
                                   '주소:' + str(map_db.iloc[i]['addr3'])+ '<br>' +
                                   '메뉴:' + str(map_db.iloc[i]['menu'])                    
                        )
            popup = folium.Popup(iframe, min_width=200, max_width=200)
            folium.Marker([map_db.iloc[i]['y_code'], map_db.iloc[i]['x_code']], popup=popup).add_to(m)

    m.save('incheon.html')

    print('--> Done make Map!')

if __name__ == '__main__':

    food_url = 'https://curryyou.tistory.com/349?category=937744'

    db = pd.read_csv('total_food_store_info.csv', encoding='cp949')
    col = 'addr1'                  # board_category / food_category1 / food_category2, addr1, addr2
    category_name = '인천'                # 골목식당 / 맛녀석 / 백반기행 / 생활의달인

    make_map(db, col, category_name)

    ### 맛집 주소 만들기 API 호출 = x,y 좌표 / 도로명주소 / 카테고리
    # df = pd.read_csv('food_store_db.csv', encoding='cp949')
    # print(len(df))

    # x_coord = []
    # y_coord = []
    # food_addr = []
    # food_category = []

    # j = 0
    # for i in df['상호명']:
    #     print(j,'번','--> 상호명:', i)
    #     j += 1
    #     place = search_kakao_address(i)
    #     if len(place) <= 0:
    #         x_coord.append(0)
    #         y_coord.append(0)
    #         food_addr.append(0)
    #         food_category.append(0)
    #     else:
    #         x, y, addr, category = place[0]['x'], place[0]['y'], place[0]['road_address_name'], place[0]['category_name']
    #         x_coord.append(x)
    #         y_coord.append(y)
    #         food_addr.append(addr)
    #         food_category.append(category)

    # df['x_code'] = x_coord
    # df['y_code'] = y_coord
    # df['addr'] = food_addr
    # df['category'] = food_category

    # print(df.head())
    # df.to_csv('total_food_store_info.csv', encoding='utf-8-sig')

    ### --------------------------------------------------------------------
    





