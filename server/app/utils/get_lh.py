import PyPDF2

def get_table_number(page_text, course_code, _type):
    items = page_text.split('\n')[1:]
    checkpoint = -1
    for i in items:
        if i.startswith('Room'):
            checkpoint += 1
        if course_code.upper() in i:
            return checkpoint
    return None

def get_rooms_on_page(page):
    ret = (None, None)
    text = page.extract_text()
    items = text.split('\n')
    for i in items:
        if 'WED' in i:
            room_no = i.split('WED')[0].strip()
            if ret[0]:
                ret = (ret[0], room_no)
            else:
                ret = (room_no, None)
    return ret

def get_room_number(course_code, _type):
    
    reader = PyPDF2.PdfReader("/Users/shashank/Shashank/GitHub/DevClub/ClassGrid/server/app/utils/Room Allotment.pdf")
    
    for page in reader.pages[2:]:
        rooms_on_page = get_rooms_on_page(page)
        text = page.extract_text()
        if _type == "L":
            if course_code.upper() in text:
                _text = text.replace(f"{course_code.upper()}(T", f"")
                if course_code.upper() in _text:
                    tn = get_table_number(_text, course_code, _type)
                    return rooms_on_page[tn]
                else:
                    continue
        elif _type == "T":
            if f"{course_code.upper()}(T" in text:
                tn = get_table_number(text, course_code, _type)
                return rooms_on_page[tn]
    return None