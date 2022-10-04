import Parser

if __name__ == '__main__':
    N = int(input("Введите колличество фотографий: "))
    # список токенов и спиок id записываются в файлы, соответственно, "fileWithTokens.txt", "fileWithIds.txt", результат
    # записывается в файл result_pars.txt
    Parser.async_parse('fileWithTokens.txt', 'fileWithIds.txt', N)

