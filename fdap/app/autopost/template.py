def make_subject(sector: str, year: str, q: str):
    return f'[업종: {sector}] {year}년도 {q}분기'


def make_strong_tag(value: str):
    return f'<strong>{value}</strong>'


def make_p_tag(value: str):
    return f'<p>{value}</p>'


def make_img_tag(name: str, src: str):
    return f'<img src="{src}" alt="{name}">'


def make_new_line(repeat: int = 1):
    return '<p>&nbsp;</p>' * repeat


def replace_template_str(template: str, values: dict, parameter_format: list = None):
    import re

    if parameter_format is None:
        parameter_format = ['{{', '}}']

    re_value = None
    for key, value in values.items():
        re_key = parameter_format[0] + key + parameter_format[1]
        re_value = re.sub(re_key, value, template)

    return re_value


class Template:
    _title: str = ''
    _description: str = ''
    _image: str = ''

    def __init__(self, title: str, image: dict, description: str = ''):
        """
        Args:
            title:
            image:
            description:
        """
        self.set_title(title)
        self.set_image(image['name'], image['src'])
        self.set_description(description)

    def set_title(self, title: str):
        if title:
            self._title = make_p_tag(title)
        return self

    def set_image(self, name: str, src: str):
        if name and src:
            self._image = make_img_tag(name, src)
        return self

    def set_description(self, description: str):
        if description:
            self._description = make_p_tag(description)
        return self

    def make(self):
        res = ''
        res += self._title
        res += make_new_line(1)
        res += self._description
        res += self._image
        res += make_new_line(3)
        return res
