import requests
import pandas as pd
import time
import random
import uuid

cari = 'tv 40 inch'
url = "https://gql.tokopedia.com/graphql/SearchProductV5Query"

def get_headers():
  """Generate random user-agent & headers"""
  user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
  ]
  return {
    "User-Agent": random.choice(user_agents),
    "Content-Type": "application/json",
    "Referer": "https://www.tokopedia.com/",
    "Accept": "application/json",
    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8"
  }

# to retrieve all pages
def get_params():
  params = []
  for i in range(1, 20): # can be modified but dont set it to 1 idk
    param = "device=desktop&enter_method=normal_search&l_name=sre&navsource=home&ob=23&page={}&q={}&related=true&rows=60&safe_search=false&sc=&scheme=https&shipping=&show_adult=false&source=universe&srp_component_id=01.02.01.01&srp_keyword_position=0&srp_keyword_suggestion_method=history_sug&st=product&start={}&topads_bucket=true&unique_id=db3ff19835f0d22f4d31faa22d7af768&user_addressId=203724808&user_cityId=165&user_districtId=2169&user_id=222945455&user_lat=-6.9188293&user_long=107.5860329&user_postCode=40221&user_warehouseId=0&variants=&warehouses=".format(i, cari, (i - 1) * 60)
    params.append(param)
  return params

# to finally scrape the data from all pages
def scrape_data(param):
  payload = [
    {
        "operationName": "SearchProductV5Query",
        "variables": {
            "params": param
        },
        "query": "query SearchProductV5Query($params: String!) {\n  searchProductV5(params: $params) {\n    header {\n      totalData\n      responseCode\n      keywordProcess\n      keywordIntention\n      componentID\n      isQuerySafe\n      additionalParams\n      backendFilters\n      meta {\n        dynamicFields\n        __typename\n      }\n      __typename\n    }\n    data {\n      totalDataText\n      banner {\n        position\n        text\n        applink\n        url\n        imageURL\n        componentID\n        trackingOption\n        __typename\n      }\n      redirection {\n        url\n        __typename\n      }\n      related {\n        relatedKeyword\n        position\n        trackingOption\n        otherRelated {\n          keyword\n          url\n          applink\n          componentID\n          products {\n            oldID: id\n            id: id_str_auto_\n            name\n            url\n            applink\n            mediaURL {\n              image\n              __typename\n            }\n            shop {\n              oldID: id\n              id: id_str_auto_\n              name\n              city\n              tier\n              __typename\n            }\n            badge {\n              oldID: id\n              id: id_str_auto_\n              title\n              url\n              __typename\n            }\n            price {\n              text\n              number\n              __typename\n            }\n            freeShipping {\n              url\n              __typename\n            }\n            labelGroups {\n              position\n              title\n              type\n              url\n              styles {\n                key\n                value\n                __typename\n              }\n              __typename\n            }\n            rating\n            wishlist\n            ads {\n              id\n              productClickURL\n              productViewURL\n              productWishlistURL\n              tag\n              __typename\n            }\n            meta {\n              oldWarehouseID: warehouseID\n              warehouseID: warehouseID_str_auto_\n              componentID\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        query\n        text\n        componentID\n        trackingOption\n        __typename\n      }\n      ticker {\n        oldID: id\n        id: id_str_auto_\n        text\n        query\n        applink\n        componentID\n        trackingOption\n        __typename\n      }\n      violation {\n        headerText\n        descriptionText\n        imageURL\n        ctaURL\n        ctaApplink\n        buttonText\n        buttonType\n        __typename\n      }\n      products {\n        oldID: id\n        id: id_str_auto_\n        ttsProductID\n        name\n        url\n        applink\n        mediaURL {\n          image\n          image300\n          videoCustom\n          __typename\n        }\n        shop {\n          oldID: id\n          id: id_str_auto_\n          ttsSellerID\n          name\n          url\n          city\n          tier\n          __typename\n        }\n        stock {\n          ttsSKUID\n          __typename\n        }\n        badge {\n          oldID: id\n          id: id_str_auto_\n          title\n          url\n          __typename\n        }\n        price {\n          text\n          number\n          range\n          original\n          discountPercentage\n          __typename\n        }\n        freeShipping {\n          url\n          __typename\n        }\n        labelGroups {\n          position\n          title\n          type\n          url\n          styles {\n            key\n            value\n            __typename\n          }\n          __typename\n        }\n        labelGroupsVariant {\n          title\n          type\n          typeVariant\n          hexColor\n          __typename\n        }\n        category {\n          oldID: id\n          id: id_str_auto_\n          name\n          breadcrumb\n          gaKey\n          __typename\n        }\n        rating\n        wishlist\n        ads {\n          id\n          productClickURL\n          productViewURL\n          productWishlistURL\n          tag\n          __typename\n        }\n        meta {\n          oldParentID: parentID\n          parentID: parentID_str_auto_\n          oldWarehouseID: warehouseID\n          warehouseID: warehouseID_str_auto_\n          isImageBlurred\n          isPortrait\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
    }
  ]
  response = requests.post(url, json=payload, headers=get_headers(), timeout=10)
  
  if response.status_code == 429:
      print("Rate limited! Waiting 60s...")
      time.sleep(60)
      return scrape_data(param) 
    
  response.raise_for_status()
  rows = response.json()[0]['data']['searchProductV5']['data']['products']
  
  data = []
  for i in range(0, len(rows)):
    no = i
    product_name = rows[i]['name']
    price = rows[i]['price']['number']
    rate = rows[i]['rating']
    shop = rows[i]['shop']['name']
    location = rows[i]['shop']['city']
    
    data.append(
      (no, product_name, price, rate, shop, location)
    )
  return data

if __name__ == '__main__':
  start_time = time.time()
  print(f"[START] {time.strftime('%Y-%m-%d %H:%M:%S')}")
  
  params = get_params()
  all_data = []
  
  for i in range(0, len(params)):
    loop_start = time.time()
    param = params[i]
    data = scrape_data(param)
    all_data.extend(data)
    loop_time = time.time() - loop_start
    print(f"[PAGE {i+1}] {len(data)} products | {loop_time:.2f}s")
    
  timestamp = time.strftime('%Y%m%d_%H%M%S')
  random_id = uuid.uuid4().hex[:8]
  filename = f"res/tokped_data_{timestamp}_{random_id}.csv"
  
  df = pd.DataFrame(all_data, columns=['No', 'Nama Produk', 'Harga', 'Rating', 'Toko', 'Lokasi'])
  df.to_csv(filename, index=False)
  print(df)
  
  total_time = time.time() - start_time
  print(f"\n[COMPLETE]")
  print(f"Total data: {len(all_data)} products")
  print(f"Total time: {total_time:.2f}s ({total_time/60:.2f} minutes)")
  print(f"Avg per page: {total_time/len(params):.2f}s")