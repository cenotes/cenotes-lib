import base64
import nacl.exceptions
import nacl.secret
import pytest

from cenotes_lib import exceptions, crypto


def assert_decrypt(payload, key, plaintext):
    assert crypto.decrypt_note(payload, key).decode() == plaintext


def test_craft_key():
    crypto.craft_key_from_password("lalala".encode())
    crypto.craft_key_from_password("lalala")


def test_secret_box_crafting(testing_key):
    assert isinstance(crypto.craft_secret_box(testing_key),
                      nacl.secret.SecretBox)


def test_encrypt_decrypt():
    password = "test"
    plaintext = "can you see me?"
    key = crypto.craft_key_from_password(password)
    box1 = crypto.craft_secret_box(key)
    box2 = crypto.craft_secret_box(key)
    ciphertext = box1.encrypt(plaintext.encode())
    assert box2.decrypt(ciphertext).decode() == plaintext


def test_encrypt_with_box(testing_box):
    plaintext = "can you see me?"
    assert crypto.encrypt_with_box(plaintext, testing_box) != plaintext


def test_decrypt_with_box(testing_box):
    plaintext = "can you see me?"
    ciphertext = crypto.encrypt_with_box(plaintext, testing_box)
    assert (crypto.decrypt_with_box(ciphertext, testing_box).decode()
            == plaintext)


def test_decrypt_with_box_wrong_password(testing_box):
    plaintext = "can you see me?"
    ciphertext = crypto.encrypt_with_box(plaintext, testing_box)
    with pytest.raises(exceptions.CenotesError):
        crypto.decrypt_with_box(ciphertext, crypto.craft_secret_box(
            crypto.craft_key_from_password("mallory")))


def test_encrypt_with_password():
    plaintext = "can you see me?"
    password = "test"
    assert crypto.encrypt_with_password(plaintext, password) != plaintext


def test_decrypt_with_key():
    plaintext = "can you see me?"
    password = "test"
    assert crypto.decrypt_with_key(*crypto.encrypt_with_password(
        plaintext, password)).decode() == plaintext


def test_key_encrypt_decrypt():
    plaintext = "can you see me?"
    key = crypto.craft_key_from_password("test")
    assert (crypto.decrypt_with_key(
        crypto.encrypt_with_key(
            plaintext, key), key).decode() == plaintext)


def test_generate_random_chars():
    random_chars = crypto.generate_random_chars(15)
    assert isinstance(random_chars, bytes)
    assert len(random_chars) == 15


def test_generate_url_safe_pass():
    assert isinstance(crypto.generate_url_safe_pass(), str)


def test_url_safe_encode():
    text = "test me|"
    assert crypto.url_safe_encode(text) != text.encode()


def test_url_safe_decode():
    text1 = "test me"
    text2 = "test me|||"

    assert (crypto.url_safe_encode(text1)
            == base64.b64encode(text1.encode()).decode())
    assert (crypto.url_safe_decode(crypto.url_safe_encode(text2)).decode()
            == text2)


def test_encrypt_note():
    text1 = "test me"
    password = "1"
    payload, key = crypto.encrypt_note(text1, password)
    assert text1 != payload
    assert password != key


def test_encrypt_note_empty_text():
    text = ""
    password = "1"
    payload, key = crypto.encrypt_note(text, password)
    assert_decrypt(payload, key, text)


def test_encrypt_note_empty_password():
    text1 = "test me"
    payload, key = crypto.encrypt_note(text1)
    assert text1 != payload


def test_decrypt_note():
    text1 = "test me"
    password = "1"
    payload, key = crypto.encrypt_note(text1, password)
    assert_decrypt(payload, key, text1)


def test_decrypt_note_empty_password():
    text1 = "test me"
    payload, key = crypto.encrypt_note(text1)
    assert_decrypt(payload, key, text1)


def test_decrypt_note_wrong_pass():
    text1 = "test me"
    password = "1"
    payload, key = crypto.encrypt_note(text1, password)
    with pytest.raises(exceptions.CenotesError):
        crypto.decrypt_note(payload, "wrong?")


def test_encrypt_with_unsupported_algorithm():
    with pytest.raises(exceptions.InvalidUsage):
        crypto.encrypt_note_with_params("test", "123", "crazy_alg", "min")


def test_encrypt_with_unsupported_algorithm_options():
    with pytest.raises(exceptions.InvalidUsage):
        crypto.encrypt_note_with_params("test", "123", "scrypt", "invalid")


def test_encrypt_with_params():
    text = "test123"
    payload, key = crypto.encrypt_note_with_params(text, "123", "scrypt",
                                                   "min")
    assert_decrypt(payload, key, text)


def test_decrypt_note_with_formatting():
    text1 = ("test me\n"
             "with extra lines\n"
             "and a few more\n")
    password = "1"
    payload, key = crypto.encrypt_note(text1, password)
    assert_decrypt(payload, key, text1)
