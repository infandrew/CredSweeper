import pytest
from regex import regex


class TestRegex:
    TEST_AWS_ID = "ASCA0123456789ABCDEF"
    TEST_AWS_REGEX = regex.compile(
        "(^|[^0-9A-Za-z])(?P<value>(AROA|ASCA)[0-9A-Z]{16})([0-9A-Z]?)([^0-9A-Za-z]|$)")

    @pytest.mark.parametrize(  #
        'text',  #
        [  #
            f"{TEST_AWS_ID}XX",  # 22 symbols
            f"i{TEST_AWS_ID}",  #
            f"{TEST_AWS_ID[0:18]}",  #
            f"{TEST_AWS_ID[0:18]}x",  #
            f"{TEST_AWS_ID[0:18]}+",  #
            f"{TEST_AWS_ID[0:18]}/",  #
            f"{TEST_AWS_ID[1:19]}"  #
        ])
    def test_regex_n(self, text: str):
        assert TestRegex.TEST_AWS_REGEX.search(text) is None

    @pytest.mark.parametrize(  #
        'text',  #
        [  #
            f"{TEST_AWS_ID}",  #
            f"N={TEST_AWS_ID}",  #
            f"\"{TEST_AWS_ID}\"",  #
            f"{TEST_AWS_ID}/6/g'",  #
            f"={TEST_AWS_ID}%2F",  #
            f"sed 's/{TEST_AWS_ID}/6/g'",  #
            f"{TEST_AWS_ID}X",  #
            f"--key {TEST_AWS_ID}X --help"  #
        ])
    def test_regex_p(self, text: str):
        obtained = TestRegex.TEST_AWS_REGEX.search(text)
        assert obtained is not None
        found = False
        for i in obtained.groups():
            if TestRegex.TEST_AWS_ID == i:
                found = True
                break
        assert found
