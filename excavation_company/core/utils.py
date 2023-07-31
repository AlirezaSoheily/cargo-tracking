import jdatetime


def jalali_to_georg(jalali_date):
    year, month, day = map(lambda x: int(x), jalali_date.split('/'))
    georg = jdatetime.date(day=day, month=month, year=year).togregorian()
    return georg


def georg_to_jalali(georg_date):
    georg_date = str(georg_date)
    year, month, day = map(lambda x: int(x), georg_date.split('-'))
    jalali = jdatetime.date.fromgregorian(day=day, month=month, year=year)
    return jalali
