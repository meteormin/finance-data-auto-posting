def make_template(sector: str, year: str, q: str):
    return f'{sector}: {year}년도 {q}분기'


def make_img_tag(name: str, src: str):
    return f'<p>{name}</p><img src={src}>' + ('<p>&nbsp;</p>' * 3)
