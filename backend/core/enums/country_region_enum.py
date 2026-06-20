from enum import Enum


class Region(Enum):
    CRIMEA = 'CRIMEA'
    VINNYTSIA = 'VINNYTSIA'
    VOLYN = 'VOLYN'
    DNIPRO = 'DNIPRO'
    DONETSK = 'DONETSK'
    IVANO_FRANKIVSK = 'IVANO-FRANKIVSK'
    KHERSON = 'KHERSON'
    KHMELNYTSKYI = 'KHMELNYTSKYI'
    KYIV = 'KYIV'
    KIROVOHRAD = 'KIROVOHRAD'
    LUHANSK = 'LUHANSK'
    LVIV = 'LVIV'
    MYKOLAIV = 'MYKOLAIV'
    ODESA = 'ODESA'
    POLTAVA = 'POLTAVA'
    RIVNE = 'RIVNE'
    SUMY = 'SUMY'
    TERNOPIL = 'TERNOPIL'
    KHARKIV = 'KHARKIV'
    ZAPORIZHZHIA = 'ZAPORIZHZHIA'
    ZHYTOMYR = 'ZHYTOMYR'
    CHERKASY = 'CHERKASY'
    CHERNIVTSI = 'CHERNIVTSI'
    CHERNIHIV = 'CHERNIHIV'

    @classmethod
    def choices(cls):
        return [(item.value, item.value) for item in cls]