import os
import sys
from unittest import TestCase

import apimoex
import requests

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "Implementation"
    )
)
from Markets.MoexQuoteProviderTest import sampleQuoteData


class ApiMoexTest(TestCase):

    __session = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.__session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        pass
        # cls.__session.close()

    def testStockQuotesFeed(self):
        self.__session.get(
            'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/GAZP.json',
            params={'iss.only': 'history,history.cursor', 'history.columns': 'BOARDID,TRADEDATE,CLOSE,VOLUME,VALUE'}
        )
        # res = apimoex.get_board_history(
        #     self.__session,
        #     'GAZP',
        #     '2022-10-09',
        #     '2022-10-10',
        #     ('TRADEDATE', 'CLOSE'),
        #     'TQBR'
        # )
        for expectedQuote in sampleQuoteData:
            pass
            # with self.subTest(f"GAZP @ {expectedQuote['TRADEDATE']}"):
            #     self.assertIn(
            #         expectedQuote,
            #         apimoex.get_board_history(
            #             self.__session,
            #             'GAZP',
            #             '2022-01-07',
            #             '2022-10-10',
            #             ('TRADEDATE', 'CLOSE'),
            #             'TQBR'
            #         )
            #     )
