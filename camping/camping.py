import urllib
import json
import pprint
import requests as req
import pandas as pd
import folium


def get_camping_API(url, service_key):

    # service_key = 'FIw33cX7LX7F%2Fiid8sB5vMhoBUL%2FCfKt%2F2PnMSvzFC%2F%2BSQboKJ0nozbOSVjLyQWLp3FVkXpeyGubCmoOUONNjg%3D%3D'
    # url = 'http://apis.data.go.kr/B551011/GoCamping'
    url = 'https://apis.data.go.kr/B551011/GoCamping/basedList?serviceKey=FIw33cX7LX7F%2Fiid8sB5vMhoBUL%2FCfKt%2F2PnMSvzFC%2F%2BSQboKJ0nozbOSVjLyQWLp3FVkXpeyGubCmoOUONNjg%3D%3D&numOfRows=3245&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json'
    response = req.get(url, verify=False)
    contents = response.text
    #print(contents)

    pp = pprint.PrettyPrinter(indent=4)
    #print(pp.pprint(contents))
    json_ob = json.loads(contents)
    #print(type(json_ob))

    body = json_ob['response']['body']['items']['item']
    # print(body)

    df = pd.json_normalize(body)
    # print(df)
    df = pd.DataFrame(df)
    # # print(df)
    df.to_csv('D:/python_basic/camping/camping_db.csv', encoding='utf-8-sig')

    return df

def make_map(db):

    col_list_unique = db['doNm'].unique() 
    print(col_list_unique)    
    
    select_col = input('선택 지역:')

    transfer_name = {'전라남도':'JeonNam', '강원도':'KangWon', '경상남도':'GyeongNam',
                     '경상북도':'GyeongBok', '제주도':'Jeju', '충청남도':'ChungNam', 
                     '경기도':'GyeongGi', '인천시':'Incheon', '충청북도':'ChungBok',
                     '전라북도':'JenonBok', '대구시':'DaeGu', '서울시':'Seoul', '광주시':'GwangJu',
                     '울산시':'Ulsan', '부산시':'Busan', '대전시':'DaeJeon', '세종시':'Sejong'}

    m = folium.Map(location=[35.809747, 127.092337], zoom_start=13)
    
    make_db = db[db['doNm'] == select_col]

    for i in range(len(make_db)):
            iframe = folium.IFrame('캠핑장명:' + str(make_db.iloc[i]['facltNm']) + '<br>' +
                                   '운영:'+ str(make_db.iloc[i]['facltDivNm']) + '<br>' +
                                   '타입:' + str(make_db.iloc[i]['induty']) + '<br>' +
                                   '주소:' + str(make_db.iloc[i]['addr1']) + '<br>' +
                                   '홈페이지:' + str(make_db.iloc[i]['homepage'])
                                   )
            popup = folium.Popup(iframe, min_width=300, max_width=300)
            folium.Marker([make_db.iloc[i]['mapY'], make_db.iloc[i]['mapX']], popup=popup).add_to(m)        
    
    m.save(transfer_name[select_col]+'_'+str(len(make_db)) + '.html')

    return print('done make map!')


if __name__ == '__main__':
    
    camp_df = pd.read_csv('D:/python_basic/camping/camping_db.csv', encoding='cp949')

    print(camp_df.columns)

    # facltNm / facltDivNm / induty / lctCl / doNm / sigunguNm / addr1 / mapX / mapY / tel / homepage / resveUrl 

    df = camp_df[['facltNm', 'facltDivNm', 'induty', 'lctCl', 'doNm', 'sigunguNm', 'addr1', 'mapX', 
                   'mapY', 'tel', 'homepage', 'resveUrl']]

    print(df.head())


    make_map(df)
    