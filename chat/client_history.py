"""
Chat project

History of client messages

copyrighted by viktor.bushmin@gmail.com
"""

import uuid
import ipaddress
import json

import logging


class ClientRecord:
    """
    class holds client record attributes and data
    """
    _clientLogin: str = None

    _clientIP: ipaddress

    _clientUUID: uuid

    _clientData: None

    __recordUUID: str = None

    ZERO_IP = ipaddress.ip_address('0.0.0.0')  # in Chat we have no ALL user
    ZERO_UUID = uuid.UUID('00000000-0000-0000-0000-000000000000')

    def __init__(self):
        self.__recordUUID = uuid.uuid4()
        logging.debug(f'recordUUID', self.__recordUUID)

        self._clientLogin = 'Undefined'
        self._clientIP = self.ZERO_IP
        self._clientUUID = self.ZERO_UUID
        self._clientData = None

    @property
    def client_login(self):
        logging.debug(f'get clientName {self._clientLogin}')
        return self._clientLogin

    @client_login.setter
    def client_login(self, value):
        if len(value) > 0:
            logging.debug(f'set clientLogin to {value}')
            self._clientLogin = value
        else:
            logging.error('can not set value of clientLogin to nothing, value should contain at list one symbol', value)
            raise Valueerror('Login length should be greater than zero')

    @property
    def client_ip(self):
        logging.debug(f'get clientIP', self._clientIP)
        return self._clientIP

    @client_ip.setter
    def client_ip(self, value):
        if ipaddress.ip_address(value) > self.ZERO_IP:
            logging.debug(f'set clientIP to {value}')
            self._clientIP = value
        else:
            err_msg = f'clientIP can not be {self.ZERO_IP}'
            logging.error(err_msg)
            raise Valueerror(err_msg)

    @property
    def client_uuid(self):
        logging.debug(f'get client_uuid', self._clientUUID)
        return self._clientUUID

    @client_uuid.setter
    def client_uuid(self, value):
        if value > self.ZERO_UUID:
            logging.debug(f'set client_uuid to {value}')
            self._clientUUID = value
        else:
            err_msg = f'clientUUID can not be {self.ZERO_UUID}'
            logging.error(err_msg)
            raise Valueerror(err_msg)

    @property
    def client_data(self):
        logging.debug(f'get clientData from record {self.__recordUUID}')
        return self._clientData

    @client_data.setter
    def client_data(self, value):
        if value is not None:
            logging.debug(f'set clientData of the record {self.__recordUUID} to ', value)
            self._clientData = value
        else:
            err_msg = f'Due to Value error can not set clientData to {self.__recordUUID}'
            raise Valueerror(err_msg)
            logging.error(err_msg, value)

    def __str__(self):
        result_string = f'clientLogin: {self._clientLogin},' + \
                        f'clientIP: {self._clientIP}, ' + \
                        f'clientUUID: {self._clientUUID}, ' + \
                        f'clientData: {self._clientData}'
        logging.debug(f'from ClientRecord to __str__ result is ', result_string)
        return result_string

    def __dict__(self):
        result = {'clientIP': str(self._clientIP),
                  'clientUUID': str(self._clientUUID),
                  'clientLogin': self._clientLogin,
                  'clientData': self.client_data}
        return result

    def to_json(self):
        """
        Make json from ClientRecord
        :return: json object as described otherwise return None
        """
        result_json: json

        try:
            result_json = json.dumps(self.__dict__())
            logging.debug(f'from ClientRecord to json result is ', result_json)
        except:  # todo specify exceptions
            logging.error(f'JSON for ClientRecord {self.__recordUUID} could not be made due to errors', exc_info=True)
        return result_json


class ClientHistory:
    records: list

    def __init__(self):
        self.records = [ClientRecord] * 0

    def add_record(self, record: ClientRecord):
        """
        Add new record to record list
        :param ClientRecord class record:
        :return: True if ClientRecord was added successfully  otherwise False
        """
        result_was_added = False

        try:
            self.records.append(record)
            result_was_added = True
        except:  # todo specify exceptions
            logging.error(f'Can not add new record ', exc_info=True)

        return result_was_added

    def get_last_record(self):
        """
        Returns last element in self.records list

        :return: last record of ClientRecord class otherwise returns None
        """
        result_record = None
        try:
            if len(self.records) > 0:
                result_record = self.records[-1]
        except:  # todo specify exceptions
            logging.error(f'Can not get last record ', exc_info=True)

        return result_record

    def to_str(self):
        result_string = 'No data in history\n'

        try:
            if len(self.records) > 0:
                for record in self.records:
                    result_string += f'\n {record}'
            else:
                result_string += 'Start talking to fill this history!\n'

        except:  # todo specify exceptions
            logging.error(f'Can not make __str__ from ClientHistory class ', exc_info=True)

        return result_string