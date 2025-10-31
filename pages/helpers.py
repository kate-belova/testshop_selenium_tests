def assert_element_is_displayed_and_enabled(element):
    assert element.is_displayed(), f'Element is not displayed: {element}'
    assert element.is_enabled(), f'Element is not enabled: {element}'


def assert_product_price(actual_price, expected_price):
    assert actual_price == expected_price, (
        f'Product price should be "{expected_price}", '
        f'but actual price is "{actual_price}"'
    )


def assert_product_title(actual_title, expected_title):
    assert actual_title == expected_title, (
        f'Product title should be "{expected_title}", '
        f'but got "{actual_title}"'
    )


def assert_products_count(actual, expected):
    actual_int = int(actual) if isinstance(actual, str) else actual
    expected_int = int(expected) if isinstance(expected, str) else expected

    assert (
        actual_int == expected_int
    ), f'Products count should be {expected_int}, but got {actual_int}'


def assert_search_counter_and_actual_amount_found(
    counter_number, actual_number
):
    assert counter_number == actual_number, (
        f'Search counter is {counter_number}, '
        f'but actual number of products is {actual_number}'
    )


def assert_text(actual, expected):
    assert actual == expected, f'Text should be {expected}, but got {actual}'


def assert_word_in_title(word, title):
    assert (
        word.lower() in title.lower()
    ), f'Title should contain {word}, but actual title is {title}'


def get_expected_text_in_product_url_from_product_title(product_title):
    url_text = product_title.lower().strip()
    url_text = url_text.replace(' ', '-')

    return url_text
