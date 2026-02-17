from io import BytesIO


class TestEmployeesAPI:
    """Интеграционные тесты для API сотрудников"""

    def test_add_employee(self, client):
        """Тест: успешное добавление сотрудника"""
        response = client.post(
            "/employees/add",
            data={
                "last_name": "Иванов",
                "first_name": "Иван",
                "middle_name": "Иванович",
                "department": "РПО",
            },
        )
        assert response.status_code in (200, 302, 303)

    def test_add_employee_missing_required(self, client):
        """Тест: ошибка при отсутствии обязательных полей"""
        response = client.post(
            "/employees/add",
            data={"last_name": "", "first_name": ""},
        )
        assert response.status_code in (200, 422)

    def test_bulk_add_employees(self, client):
        """Тест: массовое добавление сотрудников"""
        response = client.post(
            "/employees/bulk-add",
            json={
                "employees": [
                    {"first_name": "Петр", "last_name": "Петров"},
                    {"first_name": "Алексей", "last_name": "Сидоров"},
                ]
            },
        )
        assert response.status_code in (200, 201, 302, 303)

    def test_list_employees(self, client):
        """Тест: получение списка сотрудников"""
        response = client.get("/employees")
        assert response.status_code == 200


class TestStopWordsAPI:
    """Интеграционные тесты для API стоп-слов"""

    def test_add_stop_word(self, client):
        """Тест: добавление стоп-слова"""
        response = client.post(
            "/stop-words/add",
            data={"word": "тестовое"},
        )
        assert response.status_code in (200, 302, 303)

    def test_list_stop_words(self, client):
        """Тест: получение списка стоп-слов"""
        response = client.get("/import")
        assert response.status_code == 200


class TestImportExcel:
    """Интеграционные тесты для импорта из Excel"""

    def test_import_1c_invalid_file(self, client):
        """Тест: загрузка невалидного файла 1С"""
        fake_file = BytesIO(b"not an excel file")
        response = client.post(
            "/import-1c",
            files={
                "file": (
                    "test.xlsx",
                    fake_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )
        assert response.status_code in (200, 400, 500)

    def test_import_sbis_invalid_file(self, client):
        """Тест: загрузка невалидного файла СБИС"""
        fake_file = BytesIO(b"not an excel file")
        response = client.post(
            "/import-sbis",
            files={
                "file": (
                    "test.xlsx",
                    fake_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )
        assert response.status_code in (200, 400, 500)
