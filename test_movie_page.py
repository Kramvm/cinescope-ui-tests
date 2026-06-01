import allure
import pytest
from datetime import datetime

from page_object_models import CinescopMoviePage, CinescopLoginPage

CANDIDATE_MOVIE_IDS = [2450, 2449, 2448, 2447, 2446, 2445]


@allure.epic("Тестирование UI")
@allure.feature("Тестирование страницы фильма")
@pytest.mark.ui
class TestMoviePage:

    @allure.story("Отзывы под фильмом")
    @allure.title("Оставление отзыва под фильмом")
    def test_leave_review(self, ui_page, registered_user):
        review_text = f"Отличный фильм, всем советую! [{datetime.now().strftime('%H:%M:%S')}]"

        with allure.step("Авторизация пользователя"):
            login_page = CinescopLoginPage(ui_page)
            login_page.open()
            login_page.login(registered_user.email, registered_user.password)
            login_page.assert_was_redirect_to_home_page()
            login_page.assert_allert_was_pop_up()

        with allure.step("Выбор доступного фильма для отзыва"):
            movie_page = CinescopMoviePage(ui_page)
            movie_id = None
            for candidate_id in CANDIDATE_MOVIE_IDS:
                movie_page.open(candidate_id)
                if movie_page.has_review_form():
                    movie_id = candidate_id
                    break
            assert movie_id is not None, "Не найден фильм с доступной формой отзыва"

        with allure.step(f"Оставление отзыва на фильм #{movie_id}"):
            movie_page.enter_review(review_text)
            movie_page.submit_review()

        movie_page.assert_review_is_visible(review_text)
        movie_page.make_screenshot_and_attach_to_allure()
