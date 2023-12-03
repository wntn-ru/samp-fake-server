import socket
import struct


class SampServer:
    def __init__(self, ip: str = '0.0.0.0', port: int = 7777):
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )
        self.server.bind((ip, port))
        
    def handle(self):
        data, addr = self.server.recvfrom(32)
        if data[0:4].decode('utf-8') != 'SAMP':
            return
        # octets = [str(octet) for octet in data[4:8]]
        # server_ip = '.'.join(octets)
        # server_port = data[8] + (data[9] << 8)
        opcode = chr(data[10])
        match opcode:
            case 'p':
                response = data
                self.server.sendto(response, addr)
            
            case 'c':
                players = [
                    ['dimiano', 0],
                    ['dimiano', 0],
                    ['dimiano', 0],
                    ['dimiano', 0],
                    ['dimiano', 0],
                    ['dimiano', 0],
                    ['dimiano', 0],
                    ['dimiano', 0],
                    ['dimiano', 0],
                    ['dimiano', 0]
                ] 
                response = data[0:11] + struct.pack('<H', len(players))
                for player in players:
                    response += struct.pack(f'<B{len(player[0])}sI', len(player[0]), bytes(player[0], 'utf-8'), player[1])
                self.server.sendto(response, addr)
            
            case 'r':
                rules = {
                    'weburl': 'https://wntn.ru/',
                    'favorite-language': 'python'
                }
                response = data[0:11] + struct.pack('<H', len(rules))
                for rule, value in rules.items():
                    response += struct.pack(f'<B{len(rule)}sB{len(value)}s', len(rule), bytes(rule, 'utf-8'), len(value), bytes(value, 'utf-8'))
                self.server.sendto(response, addr)
            
            case 'i':
                password = True
                current_players = 0
                max_players = 0
                hostname = bytes(addr[0], 'cp1251')
                gamemode = bytes('fake server', 'cp1251')
                language = bytes('python', 'cp1251')
                response = data[0:11] + struct.pack(
                    f'<bHHI{len(hostname)}sI{len(gamemode)}sI{len(language)}s',
                    password,
                    current_players,
                    max_players,
                    len(hostname),
                    hostname,
                    len(gamemode),
                    gamemode,
                    len(language),
                    language
                )
                self.server.sendto(response, addr)


def main():
    server = SampServer()
    while True:
        try:
            server.handle()
        except KeyboardInterrupt:
            break
        except Exception:
            pass

if __name__ == '__main__':
    main()