
#띄어쓰기 개수 세기
def count_space(sentence):
    return sentence.count(' ')
#단모음 + 단자음 개수 세기
def count_single_letter(sentence):
    ja = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ','ㄳ','ㄵ','ㄶ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅄ']
    mo = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
    cnt = 0
    for ch in sentence:
        if(ch in ja or ch in mo):
            cnt += 1
    return cnt

while True:
    sentence = input("문장 입력:")
    if sentence == "":
        break
    print("띄어쓰기 개수:", count_space(sentence))
    print("단자음 단모음 개수:", count_single_letter(sentence))
