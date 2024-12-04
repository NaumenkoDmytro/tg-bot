import hashlib
import hmac
import requests
import time
import base64
from urllib.parse import quote


class AmazonShortenLink:
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 associate_tag: str):
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__associate_tag = associate_tag

    def __generate_paapi_signature(self, original_url):
        """
        Генерация подписи для Amazon Product Advertising API
        """
        # Настройки API
        host = "webservices.amazon.com"
        region = "us-east-1"
        endpoint = f"https://{host}/paapi5/getitems"

        # Формирование тела запроса
        payload = {
            "PartnerTag": self.__associate_tag,
            "PartnerType": "Associates",
            "Marketplace": "www.amazon.com",
            "Items": [
                {"ASIN": self.__extract_asin(original_url)}
            ],
            "Resources": [
                "ItemInfo.Title",
                "ItemInfo.ByLineInfo",
                "Offers.Listings.Price"
            ]
        }

        # Создание строки для подписи
        canonical_request = f"POST\n/paapi5/getitems\n\nhost:{host}\n\nhost\n{hashlib.sha256(str(payload).encode('utf-8')).hexdigest()}"
        string_to_sign = f"AWS4-HMAC-SHA256\n{time.strftime('%Y%m%dT%H%M%SZ')}\n{time.strftime('%Y%m%d')}/{region}/execute-api/aws4_request\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"

        # Генерация ключей
        date_key = hmac.new(f"AWS4{self.__secret_key}".encode('utf-8'), time.strftime('%Y%m%d').encode('utf-8'),
                            hashlib.sha256).digest()
        region_key = hmac.new(date_key, region.encode('utf-8'), hashlib.sha256).digest()
        service_key = hmac.new(region_key, "execute-api".encode('utf-8'), hashlib.sha256).digest()
        signing_key = hmac.new(service_key, "aws4_request".encode('utf-8'), hashlib.sha256).digest()

        # Генерация подписи
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

        # Заголовки
        headers = {
            "Content-Type": "application/json",
            "X-Amz-Date": time.strftime('%Y%m%dT%H%M%SZ'),
            "Authorization": f"AWS4-HMAC-SHA256 Credential={self.__access_key}/{time.strftime('%Y%m%d')}/{region}/execute-api/aws4_request, SignedHeaders=host, Signature={signature}"
        }

        return endpoint, headers, payload

    @staticmethod
    def __extract_asin(url):
        try:
            parts = url.split("/")
            index = parts.index("dp")
            return parts[index + 1]
        except ValueError:
            raise ValueError("Invalid Amazon URL: Unable to extract ASIN.")

    def shorten_amazon_link(self, original_url):
        """
        Сокращение ссылки Amazon через PA API
        """
        endpoint, headers, payload = self.__generate_paapi_signature(original_url)

        # Отправка запроса
        response = requests.post(endpoint, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("ItemsResult", {}).get("Items", [{}])[0].get("DetailPageURL")
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            return original_url
