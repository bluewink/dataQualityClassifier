# 한 줄의 에러 갯수 카운트
def find_dict(one_line):
    cnt = 0
    errorfre_list = []
    f = open('dict.txt', 'r', encoding='utf-8')
    while True:
        error_word = f.readline()
        error_word = error_word.strip()
        if not error_word:
            break
        cnt = cnt + one_line.count(error_word)

        # 에러 단어 리스트 반환
        if one_line.count(error_word) == 1:
            errorfre_list.append(error_word)

        elif one_line.count(error_word) > 1:
            i = error_word * one_line.count(error_word)
            for x in list(i):
                errorfre_list.append(x)
    f.close()
    return cnt, errorfre_list
