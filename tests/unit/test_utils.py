from datetime import date, datetime
from src.main import (
    normalize_contractor_name,
    format_contractor_name,
    parse_datetime,
    parse_date,
    parse_amount,
    add_business_days,
    get_russian_holidays,
)


class TestNormalizeContractorName:
    """Тесты для функции нормализации имени контрагента"""

    def test_remove_quotes(self):
        """Тест: удаление кавычек"""
        assert normalize_contractor_name('ТехноДрайв"СТРОЙ"') == "технодрайв стро"

    def test_remove_extra_spaces(self):
        """Тест: удаление лишних пробелов"""
        assert normalize_contractor_name("ТехноДрайв   ООО") == "технодрайв ооо"

    def test_lowercase(self):
        """Тест: приведение к нижнему регистру"""
        assert normalize_contractor_name("ТехноДрайв ООО") == "технодрайв ооо"

    def test_legal_form_at_end(self):
        """Тест: перенос юридической формы в конец"""
        result = normalize_contractor_name("ООО ТехноДрайв")
        assert result == "технодрайв ооо"

    def test_complex_name(self):
        """Тест: сложное имя с кавычками и формой"""
        result = normalize_contractor_name('ТехноДрайв"СТРОЙ"ООО')
        assert "технодрайв" in result
        assert "ооо" in result

    def test_empty_string(self):
        """Тест: пустая строка"""
        assert normalize_contractor_name("") == ""

    def test_none_value(self):
        """Тест: None значение"""
        assert normalize_contractor_name(None) is None


class TestFormatContractorName:
    """Тесты для функции форматирования имени контрагента"""

    def test_capitalize_words(self):
        """Тест: капитализация слов"""
        assert format_contractor_name("технодрайв ооо") == "ТехноДрайв ООО"

    def test_legal_forms_uppercase(self):
        """Тест: юридические формы в верхний регистр"""
        assert format_contractor_name("ооо техно") == "Техно ООО"
        assert format_contractor_name("ип иванов") == "Иванов ИП"
        assert format_contractor_name("ао компания") == "Компания АО"

    def test_mixed_forms(self):
        """Тест: смешанные формы"""
        result = format_contractor_name("техно стро ооо")
        assert "ООО" in result


class TestParseDatetime:
    """Тесты для функции парсинга даты и времени"""

    def test_parse_string_date(self):
        """Тест: парсинг строки с датой"""
        result = parse_datetime("15.03.2024")
        assert result is not None
        assert result.year == 2024
        assert result.month == 3
        assert result.day == 15

    def test_parse_string_datetime(self):
        """Тест: парсинг строки с датой и временем"""
        result = parse_datetime("15.03.2024 14:30")
        assert result is not None
        assert result.hour == 14
        assert result.minute == 30

    def test_parse_excel_serial_date(self):
        """Тест: парсинг Excel серийной даты"""
        result = parse_datetime(45305)  # 15.03.2024
        assert result is not None
        assert result.year == 2024

    def test_parse_none(self):
        """Тест: парсинг None"""
        assert parse_datetime(None) is None

    def test_parse_empty_string(self):
        """Тест: парсинг пустой строки"""
        assert parse_datetime("") is None

    def test_parse_invalid_string(self):
        """Тест: парсинг некорректной строки"""
        assert parse_datetime("not-a-date") is None

    def test_parse_date_object(self):
        """Тест: парсинг объекта date"""
        d = date(2024, 3, 15)
        result = parse_datetime(d)
        assert result is not None
        assert result.date() == d

    def test_parse_datetime_object(self):
        """Тест: парсинг объекта datetime"""
        dt = datetime(2024, 3, 15, 14, 30)
        result = parse_datetime(dt)
        assert result == dt


class TestParseDate:
    """Тесты для функции парсинга даты"""

    def test_parse_string_date(self):
        """Тест: парсинг строки с датой"""
        result = parse_date("15.03.2024")
        assert result == date(2024, 3, 15)

    def test_parse_none(self):
        """Тест: парсинг None"""
        assert parse_date(None) is None


class TestParseAmount:
    """Тесты для функции парсинга суммы"""

    def test_parse_float(self):
        """Тест: парсинг float"""
        assert parse_amount(100.50) == 100.50

    def test_parse_int(self):
        """Тест: парсинг int"""
        assert parse_amount(100) == 100.0

    def test_parse_string_with_spaces(self):
        """Тест: парсинг строки с пробелами"""
        assert parse_amount("1 000,50") == 1000.50

    def test_parse_string_with_comma(self):
        """Тест: парсинг строки с запятой"""
        assert parse_amount("100,50") == 100.50

    def test_parse_none(self):
        """Тест: парсинг None"""
        assert parse_amount(None) is None

    def test_parse_empty_string(self):
        """Тест: парсинг пустой строки"""
        assert parse_amount("") is None


class TestAddBusinessDays:
    """Тесты для функции добавления рабочих дней"""

    def test_add_simple_days(self):
        """Тест: про добавление дней без выходных"""
        start = date(2024, 3, 15)  # пятница
        holidays = set()
        result = add_business_days(start, 1, holidays)
        assert result == date(2024, 3, 18)  # понедельник

    def test_skip_weekend(self):
        """Тест: пропуск выходных"""
        start = date(2024, 3, 15)  # пятница
        holidays = set()
        result = add_business_days(start, 2, holidays)
        assert result == date(2024, 3, 19)  # вторник

    def test_zero_days(self):
        """Тест: ноль дней"""
        start = date(2024, 3, 15)
        holidays = set()
        result = add_business_days(start, 0, holidays)
        assert result == start

    def test_negative_days(self):
        """Тест: отрицательное количество дней"""
        start = date(2024, 3, 15)
        holidays = set()
        result = add_business_days(start, -1, holidays)
        assert result == start


class TestGetRussianHolidays:
    """Тесты для функции получения праздников России"""

    def test_returns_set(self):
        """Тест: возвращает множество"""
        result = get_russian_holidays(2024)
        assert isinstance(result, set)

    def test_contains_new_year(self):
        """Тест: содержит новый год"""
        result = get_russian_holidays(2024)
        new_years = [d for d in result if d.year == 2024 and d.month == 1]
        assert len(new_years) > 0
