if __name__ == '__main__':
    import whattimeisit as wt
else:
    from . import whattimeisit as wt
import json
f = open('../config/april.json', 'r')
april_data = json.load(f)
f.close()

class AprilFoolsDay(Exception): ...

def is_april_fools_day():
    wt.update_date()
    if wt.month == 4 and wt.day == 1:
        return True, wt.year
    else:
        return False, wt.year
def event2026():
    if april_data['2026']['crash']:
        print('在april.json里可以设置游戏是否会崩溃')
        print('你可以在2026年4月1日玩这个游戏，但它会崩溃！')
        print('Today is April Fool\'s Day! The game will crash now!')
        raise AprilFoolsDay('This Game crash because Today is April Fool\'s Day!')

def main() -> None:
    is_april, year = is_april_fools_day()
    if is_april:
        print(f'今天是{year}年4月1日！')
        if str(year) in april_data.keys():
            event2026()
        else:
            print('但没有特别的事件发生。')
    else:
        print('今天不是愚人节，游戏正常运行。')

if __name__ == '__main__':
    main()