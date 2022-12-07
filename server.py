import threading
import socket

my_name = "服务器"
goal_name = "客户端"
encoding = "utf-8"
LOCAL_PORT = 8888
loop = 0


def send_my(new_socket):
    while True:
        send_data = input(my_name + ":|")
        print()
        new_socket.send(send_data.encode(encoding))


def rev_my(new_socket):
    global loop
    while True:
        try:
            rev_data = new_socket.recv(1024)
        except ConnectionError as e:
            print("\n客户端已断开连接")
            loop = 1
            break
        print("\n")
        print("%s:|%s".rjust(37, " ") % (rev_data.decode(encoding), goal_name))
        print(my_name + ":|", end="")


def menu():
    print("udp_socket服务器通信器".center(50, " "))


def main():
    # 1.菜单提示
    menu()
    # 2.创建套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 3.关联本地端口
    tcp_socket.bind(("", LOCAL_PORT))
    # 4.设置监听模式
    tcp_socket.listen(128)
    # 5.等待客户端连接
    while True:
        print("=" * 50)
        print("等待客户端连接...")
        new_socket, new_client_address = tcp_socket.accept()
        print("一个客户端已连接")
        # 6.创建子线程发送数据
        send_t = threading.Thread(target=send_my, args=(new_socket,))
        # 7.创建子线程接收数据
        rev_t = threading.Thread(target=rev_my, args=(new_socket,))
        # 8.线程开始
        rev_t.start()
        send_t.start()
        # 9.关闭局部套接字
        global loop
        while loop == 0:
            pass
        loop = 0
        new_socket.close()


if __name__ == '__main__':
    main()


