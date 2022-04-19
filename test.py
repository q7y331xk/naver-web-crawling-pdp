import re

test_text = "스노우피크 팔3 프로에어 제품 입니다 아틀라스 원합니다 베스티블 만원 3 이너텐트로 쓰려고 구매했으나 한번도 사용 안했구요 집에서 이너텐트 체결, 그시 체결만 해보고 다시 넣어뒀습니다 그라운드시트 스노우피크 정품 전용 그시입니다 아틀라스 베스티블 이너텐트 말고도 단독으로 사용하셔도 괜찮은 텐트라고 알고 있습니다 더블월 구조이구요 현재 국내 판매는 안하는걸로 알고 있습니다 꼭 구매 하실분만 연락 주세요 일괄 판매합니다 판매금액 : 65만원 전북 익산 직거래 택배 노리턴 착불입니다"

def main_find_cost(main_text):
    found_cost = 0
    won= r"[0-9]+원"
    man= r"[0-9]+만"
    find_num_won = re.search(won, main_text)
    find_num_man = re.search(man, main_text)
    if find_num_won:
        found_cost = int(find_num_won.group().replace('원',''))
    if find_num_man:
        found_cost = int(find_num_man.group().replace('만',''))
    return found_cost

main_find_cost(test_text)