# p2p_api.py

import requests
import logging
import time
import hmac
import hashlib
from urllib.parse import urlencode


class P2PAPIConnector:
    def __init__(self, api_key, api_secret, timeout=10):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.base_url = "https://api.binance.com"
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        })

        self.logger = logging.getLogger("FSE.P2P.API")


    def _generate_signature(self, params):
        query = urlencode(params)
        return hmac.new(
            self.api_secret,
            query.encode(),
            hashlib.sha256
        ).hexdigest()


    def _request(self, method, endpoint, params=None):
        """
        ሁሉንም API requests የሚያስተዳድር
        """

        try:
            params = params or {}

            params["timestamp"] = int(time.time() * 1000)

            params["signature"] = self._generate_signature(params)

            url = self.base_url + endpoint


            if method == "GET":
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )

            elif method == "POST":
                response = self.session.post(
                    url,
                    json=params,
                    timeout=self.timeout
                )

            else:
                raise ValueError(
                    f"Unsupported method {method}"
                )


            response.raise_for_status()

            return response.json()


        except requests.Timeout:
            self.logger.error(
                "API timeout"
            )

        except requests.HTTPError as error:
            self.logger.error(
                f"HTTP Error: {error}"
            )

        except Exception as error:
            self.logger.exception(
                f"Unexpected error: {error}"
            )

        return None


    def get_p2p_orders(self, trade_type, asset, fiat):
        """
        P2P የገበያ መረጃ መፈለጊያ
        """

        payload = {
            "tradeType": trade_type,
            "asset": asset,
            "fiat": fiat
        }

        self.logger.info(
            f"Searching {asset}/{fiat} {trade_type}"
        )

        return self._request(
            "POST",
            "/p2p/search",
            payload
        )


    def place_order(self, order_id, amount):
        """
        ትዕዛዝ ማስገቢያ
        """

        payload = {
            "orderId": order_id,
            "amount": amount
        }

        self.logger.info(
            f"Creating order {order_id}"
        )

        return self._request(
            "POST",
            "/p2p/order",
            payload
        )
