from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import uuid
import logging

"""
second task homework imports

"""

from chat.client_history import ClientRecord
from chat.client_history import ClientHistory

class Client(Protocol):
    ip: str = None
    login: str = None
    uuid: str = None
    factory: 'Chat'
    client_history_store: ClientHistory

    def __init__(self, factory):
        """
        Инициализация фабрики клиента
        :param factory:
        """
        self.factory = factory
        self.client_history_store = ClientHistory

    def __count_login_in_clients__(self, login: str):
        """
        К домашке
        Counts login string in self.factory.clients list
        :return: Counter of self.logins by login, 0 if none, -1 if error expected
        """
        res_count_login = 0

        try:
            if len(self.factory.clients):
                for next_client in self.factory.clients:
                    if login == next_client.login:
                        res_count_login += 1

            return res_count_login
        except:
            return -1



    def __user_exists__(self):
        """
        К домашке
        Check user's login in client list
        :return: True when exists otherwise False
        """
        is_user_exists = False

        if len(self.factory.clients) > 0:
            print(f"Server is checking new user {self.login} with IP {self.ip}...\n ")

            user_login_count = self.__count_login_in_clients__(self.login)
            print(f"Users with login {self.login} are {user_login_count}\n")

            is_user_exists = user_login_count >= 2

            if is_user_exists:
                print(f"User {self.login} has been registered earlier and can not be registered again\n")
            else:
                print(f"Registering user {self.login}...\n")

        return is_user_exists

    def connectionMade(self):
        """
        Обработчик подключения нового клиента
        """
        self.ip = self.transport.getHost().host
        self.uuid = uuid.uuid4()

        print(f"Client connected: {self.ip} and uuid {self.uuid}")
        self.factory.clients.append(self)
        self.transport.write(f"New user was connected with IP {self.ip} and uuid {self.uuid}\n".encode())

    def dataReceived(self, data: bytes):
        """
        Обработчик нового сообщения от клиента
        :param data:
        """
        message = data.decode().replace('\n', '')
        cur_record: ClientRecord = ClientRecord()


        if self.login is not None:
            server_message = f"{self.login}: {message}"
            self.factory.notify_all_users(server_message)

            # second task homework
            cur_record.client_ip = self.ip
            cur_record.client_uuid = self.uuid
            cur_record.client_login = self.login
            cur_record.client_data = server_message

            self.client_history_store.add_record(self.client_history_store, record=cur_record)

            print(server_message)
        else:
            if message.startswith("login:"):
                self.login = message.replace("login:", "")

                """
                Тут дальше ДЗ
                """
                if not self.__user_exists__():
                    notification = f"New user connected: {self.login}"
                    self.factory.notify_all_users(notification)

                    user_index = self.factory.clients.index(self)
                    if user_index > 0:
                        self.factory.clients[user_index].transport.write(self.client_history_store.to_str(self).encode())

                    print(notification)
                else:
                    print(f"Unrestered dubplicate user {self.login}")
                    user_index = self.factory.clients.index(self)
                    if user_index > 0:
                        self.factory.clients[user_index].transport.write(f"Unrestered dubplicate user {self.login}\n".encode())
                    print(f"Connection uuid {self.uuid} will be terminated \n")
                    self.transport.abortConnection()
                    print(f"Connection have been terminated \n")
            else:
                print("Error: Invalid client login")

    def connectionLost(self, reason=None):
        """
        Обработчик отключения клиента
        :param reason:
        """
        if self.factory.clients.count(self) > 0:
            self.factory.clients.remove(self)
        print(f"Client disconnected: {self.ip} and uuid {self.uuid}")


class Chat(Factory):
    clients: list

    def __init__(self):
        """
        Инициализация сервера
        """
        self.clients = []
        print("*" * 10, "\nStart server \nCompleted [OK]")

    def startFactory(self):
        """
        Запуск процесса ожидания новых клиентов
        :return:
        """
        print("\nServer started...")

    def buildProtocol(self, addr):
        """
        Инициализация нового клиента
        :param addr:
        :return:
        """
        return Client(self)

    def notify_all_users(self, data: str):
        """
        Отправка сообщений всем текущим пользователям
        :param data:
        :return:
        """
        for user in self.clients:
            user.transport.write(f"{data}\n".encode())


if __name__ == '__main__':
    logging.basicConfig(filename='server.log',
                        filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s -- %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.ERROR)

    logging.warning('This will get logged to a file')

    reactor.listenTCP(7410, Chat())
    reactor.run()
