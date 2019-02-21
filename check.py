import json
import requests
import pprint
import collections as cl
#食べ物の情報をとってくる函数（ぐるなびAPI）
#引数　　　fName：食べ物の名前
#　　　　　fLat ：現在地の緯度
#　　　　　fLon ：現在地の経度
#return値 レストラン情報
def getFoodsInfo(fName,fLat,fLon):
  url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"

  params={}
  params["keyid"] = "cd2b9d834b7171aec5aaa5f615692ea3"
  params["freeword"]  = fName
  params["latitude"]  = fLat
  params["longitude"]  = fLon

  #range=検索範囲の半径の大きさ(1~5)　10件以上見つかる最小の大きさを求める
  for i in range(1,6):
    params["range"]  = i
    result = requests.get(url, params)
    if(countHit(result.json())>=10):
      break

  print("range：%d" % i)
  return result.json() 

#ヒット件数を求める函数．レスポンスがエラー時の処理も行う．
#引数　　　restInfo：ぐるなびAPIが返したレストラン情報
#return値 ヒット件数
def countHit(restInfo): 
  return restInfo.get('total_hit_count', 0)
"""
def countHitOld(restInfo): 
  try:
    if(restInfo['rest']):
      hit=len(restInfo['rest'])
    else:
      hit=0
  except:
    #restInfo['rest']が読めないときエラーになる
    hit=0
    #print(restInfo['error'][0]['code'])print(restInfo['error'][0]['message'])
      
  return hit"""

#取得結果を表示する
#引数　　　restInfo：ぐるなびAPIが返したレストラン情報
#return値 void
def printFoodsInfo(restInfo):
  hitCnt=countHit(restInfo)
  for i in range(hitCnt):
    if(restInfo['rest'][i]['address']):
      print("お店情報：%d件目 / 全%d件" % (i+1,hitCnt) )
      print(restInfo['rest'][i]['address'])
      print(restInfo['rest'][i]['name'])
  

"""      
      #print(restInfo['rest'][i]['name_kana'])
      #print(restInfo['rest'][i]['opentime'])
      #print(restInfo['rest'][i]['image_url']['shop_image1'])
      #print(restInfo['rest'][i]['code']['areaname'])
      print(restInfo['rest'][i]['code']['category_name_l'][:2])
      print(" ----------------------------------------- ")
"""
if __name__=='__main__':
    data=getFoodsInfo('たこ焼き',34.986086, 135.759089)
    printFoodsInfo(data)