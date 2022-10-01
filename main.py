import Parser

if __name__ == '__main__':
    N = int(input("Введите колличество фотографий: "))
    Parser.parse('fileWithTokens.txt', 'fileWithIds.txt', N)
