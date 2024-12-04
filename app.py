from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Lista de URLs de productos
product_urls = [
    "https://www.mercadolibre.com.co/samsung-galaxy-tab-s9-fe-sm-x510nzsecoo-wifi-256gb-silver-8gb-ram-109-/p/MCO29103951#reco_item_pos=2&reco_backend=item_decorator&reco_backend_type=function&reco_client=home_items-decorator-legacy&reco_id=16d4b99b-886c-4b09-a966-38e10164ada2&reco_model=&c_id=/home/navigation-recommendations-seed/element&c_uid=2f37b679-aaed-46d6-b7c5-53b77c6c1adc&da_id=navigation&da_position=2&id_origin=/home/dynamic_access&da_sort_algorithm=ranker",
    "https://articulo.mercadolibre.com.co/MCO-1463150153-tableta-android-12-de-10-pulgadas-1920-x-1080-12-gb-de-ram-_JM#polycard_client=recommendations_pdp-pads-up&reco_backend=recos-merge-experimental-pdp-up-d_marketplace&reco_model=ranker_entity_v3&reco_client=pdp-pads-up&reco_item_pos=1&reco_backend_type=low_level&reco_id=bf2d2199-08a7-4525-b23a-4dca7ce0a1ee&is_advertising=true&ad_domain=PDPDESKTOP_UP&ad_position=2&ad_click_id=OGY4YmRmOWYtMjQ4ZS00NDljLThiMTItNDg1MDc5OGY0ZTRj",
    "https://articulo.mercadolibre.com.co/MCO-1663372660-caterpillar-cat-s48c-4gb-64gb-_JM#polycard_client=search-nordic&position=2&search_layout=stack&type=item&tracking_id=a0b2ddce-9c76-44cd-9c1a-14d883272b1d",
    "https://articulo.mercadolibre.com.co/MCO-1463150153-tableta-android-12-de-10-pulgadas-1920-x-1080-12-gb-de-ram-_JM?variation=181300519484#reco_item_pos=0&reco_backend=same-seller-rola-odin&reco_backend_type=low_level&reco_client=vip-seller_items-above&reco_id=fb318fb7-6c57-4dc0-b9f2-e92ecce8243e&reco_model=machinalis-sellers-baseline",
    "https://www.mercadolibre.com.co/galaxy-tab-s6-lite-2024-4gb-128gb-light-green-color-verde/p/MCO38017018?pdp_filters=item_id:MCO2503493650#polycard_client=recommendations_vip-pads-up&reco_backend=ranker_retrieval_system_ads_marketplace&reco_model=ranker_entity_v3&reco_client=vip-pads-up&reco_item_pos=1&reco_backend_type=low_level&reco_id=77f3edc5-00e0-4b7b-91ed-86de69bbdb63&wid=MCO2503493650&sid=recos&is_advertising=true&ad_domain=VIPDESKTOP_UP&ad_position=2&ad_click_id=NDUyN2YzM2QtMzgyNy00Yzk3LWE5ZGItNDQzNzk5YzQ4ZWY2",
    "https://articulo.mercadolibre.com.co/MCO-1484684013-tablet-pr5850-16gb-android-81-wifi-dual-sim-3g-_JM#polycard_client=recommendations_pdp-pads-up&reco_backend=recos-merge-experimental-pdp-up-d_marketplace&reco_model=ranker_entity_v3&reco_client=pdp-pads-up&reco_item_pos=2&reco_backend_type=low_level&reco_id=00d842ba-13ed-4902-a3a2-c43a04447db1&is_advertising=true&ad_domain=PDPDESKTOP_UP&ad_position=3&ad_click_id=NTc1ZjYyMjktZjAyYy00OTNkLWE3YTktMTAwMmFiMjAwZGM3",
    "https://articulo.mercadolibre.com.co/MCO-1440691937-tablet-pr6172-8-sc-1gb-16gb-3g-_JM?variation=180789117678#reco_item_pos=0&reco_backend=same-seller-rola-odin&reco_backend_type=low_level&reco_client=vip-seller_items-above&reco_id=bd2b260a-b6e6-4da8-9883-03eec097abbf&reco_model=machinalis-sellers-baseline",
    "https://articulo.mercadolibre.com.co/MCO-2695676918-tablet-android-11-32gb-2gb-10-estuche-anti-golpes-_JM#polycard_client=recommendations_vip-v2p&reco_backend=ranker_retrieval_system_org_marketplace&reco_model=ranker_entity_v3&reco_client=vip-v2p&reco_item_pos=0&reco_backend_type=low_level&reco_id=6855ee9c-24e1-4c64-844e-bf8b558ab4ad",
    "https://articulo.mercadolibre.com.co/MCO-1440817615-tablet-android-11-con-32gb-expandible-10-_JM?variation=180790463164#reco_item_pos=0&reco_backend=same-seller-rola-odin&reco_backend_type=low_level&reco_client=vip-seller_items-above&reco_id=b3a392d8-d751-4d04-80a9-d1e5f2ff5067&reco_model=machinalis-sellers-baseline",
    "https://www.mercadolibre.com.co/tablet-lenovo-tab-m10-hd-2nd-gen-tb-x306f-101-32gb-iron-gray-2gb-de-memoria-ram-y-2gb-de-memoria-ram/p/MCO18334221#polycard_client=recommendations_vip-v2p&reco_backend=ranker_retrieval_system_org_marketplace&reco_model=ranker_entity_v3&reco_client=vip-v2p&reco_item_pos=2&reco_backend_type=low_level&reco_id=f432f2f9-7d83-4a1c-88f7-518b8a495fdb&wid=MCO1418696861&sid=recos",
    "https://www.mercadolibre.com.co/xiaomi-redmi-14c-128gb-dual-sim-sage-green/p/MCO41263189?pdp_filters=item_id:MCO2721997158#polycard_client=recommendations_vip-pads-up&reco_backend=ranker_retrieval_system_ads_marketplace&reco_model=ranker_entity_v3&reco_client=vip-pads-up&reco_item_pos=2&reco_backend_type=low_level&reco_id=5820b685-3bbe-4c01-8082-e2b08e1df666&wid=MCO2721997158&sid=recos&is_advertising=true&ad_domain=VIPDESKTOP_UP&ad_position=3&ad_click_id=YzJiNjk3NmEtNjI2Yy00YTQ1LWJlMjgtZjkxMzY2YTk0NzQ3",
    "https://articulo.mercadolibre.com.co/MCO-1314537439-celular-multi-m23lite-128gb-4gb-ram-dual-sim-4g-color-negro-_JM#polycard_client=recommendations_pdp-pads-up&reco_backend=recos-merge-experimental-pdp-up-d_marketplace&reco_model=ranker_entity_v3&reco_client=pdp-pads-up&reco_item_pos=0&reco_backend_type=low_level&reco_id=8c5b7cc5-00a2-45ca-b479-a9101c01ab92&is_advertising=true&ad_domain=PDPDESKTOP_UP&ad_position=1&ad_click_id=NjQwNDk4NzYtYzljZC00YmE5LWEyODAtNTc0YTI2NzQ4NWMw",
   
]

def scrape_product(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ajusta los selectores y maneja posibles valores None
    title_element = soup.find('h1')
    price_element = soup.find('span', {'class': 'price-tag-fraction'})
    image_element = soup.find('img', {'class': 'ui-pdp-image'}) or soup.find('img')
    description_element = soup.find('p', {'class': 'ui-pdp-description__content'})

    title = title_element.text.strip() if title_element else "Título no disponible"
    price = price_element.text.strip() if price_element else "Precio no disponible"
    image = image_element['src'] if image_element else "https://via.placeholder.com/300x200.png?text=No+Image"
    description = description_element.text.strip() if description_element else "Descripción no disponible"

    return {
        'title': title,
        'price': price,
        'image': image,
        'description': description,
        'link': url
    }


@app.route('/')
def home():
    return "<h1>Bienvenido a la API de Productos</h1><p>Utiliza /api/products para obtener la lista de productos.</p>"

@app.route('/api/products', methods=['GET'])
def get_products():
    products = [scrape_product(url) for url in product_urls]
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)
