from playwright.sync_api import expect
import re


def test_dashboard_loads(page):
    """Тест: главная страница загружается"""
    page.goto("/")
    expect(page).to_have_title(re.compile(r"счет|invoice", re.IGNORECASE))


def test_dashboard_has_invoices_table(page):
    """Тест: на главной странице есть таблица счетов"""
    page.goto("/")
    table = page.locator("#invoicesTable")
    expect(table).to_be_visible()


def test_navigation_to_employees(page):
    """Тест: навигация на страницу сотрудников"""
    page.goto("/employees")
    expect(page.locator("h1, h2")).to_be_visible()


def test_navigation_to_import(page):
    """Тест: навигация на страницу импорта"""
    page.goto("/import")
    expect(page.locator("h1, h2")).to_be_visible()


def test_navigation_to_unlinked_acts(page):
    """Тест: навигация на страницу непривязанных актов"""
    page.goto("/unlinked-acts")
    expect(page.locator("h1, h2")).to_be_visible()


def test_navigation_to_linked_acts(page):
    """Тест: навигация на страницу привязанных актов"""
    page.goto("/linked-acts")
    expect(page.locator("h1, h2")).to_be_visible()


def test_delete_modal_appears(page):
    """Тест: модальное окно удаления появляется"""
    page.goto("/")
    delete_buttons = page.locator("button.btn-danger")
    if delete_buttons.count() > 0:
        delete_buttons.first.click()
        modal = page.locator("#deleteConfirmModal")
        expect(modal).to_be_visible()
        page.locator("#deleteConfirmModal .btn-secondary").click()
        expect(modal).not_to_be_visible()
