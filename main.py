import Parser
from time import time
import asyncio

if __name__ == '__main__':
    N = int(input("Введите колличество фотографий: "))
    t0 = time()
    Parser.async_parse('fileWithTokens.txt', 'fileWithIds.txt', N)
    print(time() - t0)
    t1 = time()
    Parser.parse('fileWithTokens.txt', 'fileWithIds.txt', N)
    print(time() - t1)
