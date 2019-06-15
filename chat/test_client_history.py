"""

Tests for ClientRecords and ClientHistory classes

"""
import ipaddress
import json
import unittest
import uuid

from .client_history import ClientRecord
from chat.client_history import ClientHistory


def make_client_record_from_tuple(clients: tuple, index_in_tuple: int):

        if len(clients) > 0 & (index_in_tuple > 0 & index_in_tuple < len(clients)-1):
            result_cl_rec = ClientRecord
            print(f'Dataset #{index_in_tuple} is used {clients[index_in_tuple]}')

            try:
                i = index_in_tuple
                result_cl_rec.client_ip = ipaddress.ip_address(clients[i][0][1])
                result_cl_rec.client_UUID = uuid.UUID(clients[i][1][1])
                result_cl_rec.client_Login = clients[i][2][1]
                result_cl_rec.client_data = clients[i][3][1]
            except ValueError:
                print("Exception detected ValueError it's good")

            return  result_cl_rec
# global variables ((
clients: tuple
tested_client_record: ClientRecord


clients = (
    (
        ('clientIP', '0.0.0.0'),
        ('clientUUID', '00000000-0000-0000-0000-000000000000'),
        ('clientLogin', 'Undefined'),
        ('clientData', 'new message'),
        ('result', 'good')
    ),
    (
        ('clientIP', '256.0.0.0'),
        ('clientUUID', '00600000-0000-0000-0000-000000000000'),
        ('clientLogin', 'Undefined'),
        ('clientData', 'new message'),
        ('result', 'bad')
    ),
    (
        ('clientIP', '.0.0'),
        ('clientUUID', '00000000-0000-0000-0000-000000000000'),
        ('clientLogin', 'Untiteled'),
        ('clientData', 'new message'),
        ('result', 'bad')
    ),
    (
        ('clientIP', '127.0.0.1'),
        ('clientUUID', '99b3d977-d67b-4386-91ab-22298dd26ed2'),
        ('clientLogin', 'John'),
        ('clientData', 'Hi John and little [uppet'),
        ('result', 'good')
    ),
    (
        ('clientIP', '127.0.0.1'),
        ('clientUUID', '88b3d977-d67b-4386-91ab-22298dd26ed2'),
        ('clientLogin', 'Arture'),
        ('clientData', 'Hi Arture and dfg55^&*(uppet'),
        ('result', 'good')
    ),
    (
        ('clientIP', '127.0.0.1'),
        ('clientUUID', '77b3d977-d67b-4386-91ab-22298dd26ed2'),
        ('clientLogin', 'Kate'),
        ('clientData', 'Hi Kate and kitty'),
        ('result', 'good')
    ),
)
tested_client_record = ClientRecord()
tested_client_record.client_ip = ipaddress.ip_address(clients[5][0][1])
tested_client_record.client_UUID = uuid.UUID(clients[5][1][1])
tested_client_record.client_Login = clients[5][2][1]
tested_client_record.client_data = clients[5][3][1]



class TestClientRecordsClass(unittest.TestCase):
    """
    Tests for ClientRecords class
    """


    def test_client_record_init(self):
        """
        test __init__ with all attributes and data None
        :return:
        """
        tcr = ClientRecord()


        with self.subTest('init try login'):
            self.assertEqual(tcr.client_login, clients[0][2][1])
        with self.subTest('init try uuid'):
            self.assertEqual(str(tcr.client_uuid), clients[0][1][1])
        with self.subTest(f'init try IP assert between {str(tcr.client_ip)} and {clients[0][0][1]}'):
            self.assertEqual(str(tcr.client_ip), clients[0][0][1])
        with self.subTest(f'init try data assert between {str(tcr.client_data)} and None'):
            self.assertIsNone(tcr.client_data)

    def test_client_record_setters_getters(self):
        """
        Test setters and getters in class with tuples
        result is controlled by result field
        (
                ('clientIP', '127.0.0.1'),
                ('clientUUID', '77b3d977-d67b-4386-91ab-22298dd26ed2'),
                ('clientLogin', 'Kate'),
                ('clientData', 'Hi Kate and kitty'),
                ('result', 'good')
            )
        :return:
        """
        tmp_tuple = clients
        for i in range(0, len(tmp_tuple)):
            with self.subTest(f'Try tuple #{i}'):
                try:
                    tmp_cl_rec = make_client_record_from_tuple(tmp_tuple, i)
                    self.assertEqual(tmp_cl_rec.client_ip, ipaddress.ip_address(clients[i][0][1]))
                    self.assertEqual(tmp_cl_rec.client_UUID, uuid.UUID(clients[i][1][1]))
                    self.assertEqual(tmp_cl_rec.client_Login, clients[i][2][1])
                    self.assertEqual(tmp_cl_rec.client_data, clients[i][3][1])
                except ValueError:
                    print("Exception detected ValueError it's good")

    def test_client_record_class__str__(self):
        tested_string: str
        tested_string = str(tested_client_record)
        print(tested_string)
        with self.subTest("__str__ test"):
            for i in range(0, 3):
                self.assertTrue(tested_string.find(clients[5][i][1]))

    def test_client_record_class_json(self):
        """
        result_json = {
                'login': self._clientLogin,
                'IP': self._clientIP,
                'UUID': self._clientUUID,
                'data': self._clientData
            }
        :return:
        """
        tested_json: json

        tested_json = tested_client_record.to_json()
        with self.subTest("json test, not None assert"):
            self.assertIsNotNone(tested_json)
        print('JSON is ', json.loads(tested_json))


class TestClientHistoryClass(unittest.TestCase):
    test_cr = TestClientRecordsClass

    def test_add_record_to_history(self):
        """
        We try to put some records to history
        :return:
        """
        tmp_history = ClientHistory()
        tmp_record: ClientRecord
        tmp_tuple = clients  # keywords

        for i in range(0,5):
            with self.subTest(f'History add record test with dadaset #{i}'):
                try:
                    tmp_record = make_client_record_from_tuple(tmp_tuple, i)
                    tmp_uuid = uuid.UUID(str(tmp_record.client_uuid))
                    if tmp_uuid > ClientRecord.ZERO_UUID:
                        tmp_history.add_record(tmp_record)
                        print(f'Record {tmp_record} \n\n')
                        self.assertIn(tmp_history, tmp_record)
                except ValueError:
                    print("ValueError in test_add_record_to_history detected")