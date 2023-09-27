# import socketio
# import asyncio
#
#
# # 전체 소켓 테스트 코드(클라이언트)
# async def client():
#     # 클라이언트 소켓 생성
#     sio = socketio.AsyncClient()
#
#     # 연결
#     @sio.event
#     async def connect():
#         print('connection established')
#
#     @sio.event
#     async def disconnect():
#         print('disconnected from server')
#
#
#     print("=== socket 테스트 ===")
#     print("1. back to ros")
#     print("2. back to back")
#     op = input()
#
#
#         # 서버 연결
#     await sio.connect('http://127.0.0.1:8000')
#
#         # 데이터 송신
#     if op == '1':
#         await sio.emit('testros','ros TEST')
#     elif op == '2':
#         await sio.emit('test','back TEST')
#
#
#     await sio.wait()
#
# def main(args = None):
#     asyncio.run(client())
#
# if __name__ == "__main__":
#     main()