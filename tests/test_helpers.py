import nacl.exceptions
import pytest

from cenotes_lib import exceptions, helpers


def test_enforce_bytes():
    def dummy_func(x, y, z):
        return x, y, z
    results = helpers.enforce_bytes(
        kwargs_names=["y"])(dummy_func)("test1", y="test2", z="test3")
    assert isinstance(results[0], bytes), type(results[0])
    assert isinstance(results[1], bytes), type(results[1])
    assert not isinstance(results[2], bytes), type(results[2])


def test_enforce_bytes_already_bytes():
    def dummy_func(x, y, z):
        return x, y, z
    results = helpers.enforce_bytes(
        kwargs_names=["y"])(dummy_func)("test1", y=b"test2", z="test3")
    assert isinstance(results[0], bytes), type(results[0])
    assert isinstance(results[1], bytes), type(results[1])
    assert not isinstance(results[2], bytes), type(results[2])


def test_enforce_bytes_wrong_kwarg():
    def dummy_func(x, y, z):
        return x, y, z
    with pytest.raises(SyntaxWarning):
        helpers.enforce_bytes(
            kwargs_names=["N"])(dummy_func)("test1", y="test2", z="test3")


def test_maketype():
    assert type(helpers.make_type(tuple, "lala")) == tuple
    assert type(helpers.make_type(set, "lala")) == set
    assert type(helpers.make_type(list, "lala")) == list


def test_maketuple():
    assert helpers.make_tuple("lala") == ("lala",)
    assert helpers.make_tuple(["lala"]) == ("lala",)
    assert helpers.make_tuple(("lala",)) == ("lala",)
    assert helpers.make_tuple({"lala"}) == ("lala",)


def test_safe_decryption():
    @helpers.safe_decryption
    def raise_a_crypto_error():
        raise nacl.exceptions.CryptoError("catch!")

    with pytest.raises(exceptions.CenotesError):
        raise_a_crypto_error()


def test_safe_decryption_custom_exceptions():
    @helpers.safe_decryption
    def raise_an_error():
        raise IndentationError

    with pytest.raises(IndentationError):
        raise_an_error()

    @helpers.safe_decryption(extra_exceptions=(IndentationError,))
    def raise_another_error():
        raise IndentationError

    with pytest.raises(exceptions.CenotesError):
        raise_another_error()

