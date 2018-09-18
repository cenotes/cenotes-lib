import base64
import timeit
from itertools import product
from nacl import utils as nacl_utils, secret, pwhash
from .exceptions import InvalidUsage
from .helpers import enforce_bytes, safe_decryption


def get_argon2i_params():
    # argon2i may not be supported in the current system
    try:
        return {
            "kdf": pwhash.argon2i.kdf,
            "saltbytes": pwhash.argon2i.SALTBYTES,
            "hardness": {
                "min": (pwhash.argon2i.OPSLIMIT_MIN,
                        pwhash.argon2i.MEMLIMIT_MIN),
                "interactive": (pwhash.argon2i.OPSLIMIT_INTERACTIVE,
                                pwhash.argon2i.MEMLIMIT_INTERACTIVE),
                "moderate": (pwhash.argon2i.OPSLIMIT_MODERATE,
                             pwhash.argon2i.MEMLIMIT_MODERATE),
                "sensitive": (pwhash.argon2i.OPSLIMIT_SENSITIVE,
                              pwhash.argon2i.MEMLIMIT_SENSITIVE),
            }
        }
    except AttributeError:
        return {"hardness": {}}


SUPPORTED_ALGORITHM_PARAMS = {
    "argon2i": get_argon2i_params(),
    "scrypt": {
        "kdf": pwhash.kdf_scryptsalsa208sha256,
        "saltbytes": pwhash.SCRYPT_SALTBYTES,
        "hardness": {
            "min": (pwhash.scrypt.OPSLIMIT_MIN,  pwhash.scrypt.MEMLIMIT_MIN),
            "interactive": (pwhash.scrypt.OPSLIMIT_INTERACTIVE,
                            pwhash.scrypt.MEMLIMIT_INTERACTIVE),
            "moderate": (pwhash.scrypt.OPSLIMIT_MODERATE,
                         pwhash.scrypt.MEMLIMIT_MODERATE),
            "sensitive": (pwhash.scrypt.OPSLIMIT_SENSITIVE,
                          pwhash.scrypt.MEMLIMIT_SENSITIVE)
        }
    }
}


def get_supported_algorithm_options():
    return ((algorithm,
             tuple(SUPPORTED_ALGORITHM_PARAMS[algorithm]["hardness"].keys()))
            for algorithm in SUPPORTED_ALGORITHM_PARAMS.keys())


def craft_kdf_params(algorithm="scrypt", hardness="moderate"):
    try:
        algo = SUPPORTED_ALGORITHM_PARAMS[algorithm]
        return ((algo["kdf"], nacl_utils.random(algo["saltbytes"]))
                + algo["hardness"][hardness])
    except KeyError as e:
        raise InvalidUsage(
            "{0} is not supported! Supported options are the following: {1}"
            .format(e, tuple(get_supported_algorithm_options())))


def generate_random_chars(size=32):
    return nacl_utils.random(size)


def generate_url_safe_pass(size=32):
    return base64.urlsafe_b64encode(generate_random_chars(size)).decode()


@enforce_bytes(kwargs_names="password")
def craft_key_from_password(password, kdf_params=None):
    kdf, salt, ops, mem = kdf_params or craft_kdf_params()
    return kdf(secret.SecretBox.KEY_SIZE, password, salt,
               opslimit=ops, memlimit=mem)


def craft_secret_box(key):
    return secret.SecretBox(key)


@enforce_bytes(kwargs_names="what")
def url_safe_encode(what):
    return base64.urlsafe_b64encode(what).decode()


@safe_decryption
@enforce_bytes(kwargs_names="what")
def url_safe_decode(what):
    return base64.urlsafe_b64decode(what)


@enforce_bytes(kwargs_names="what")
def encrypt_with_box(what, secret_box):
    return secret_box.encrypt(what)


@enforce_bytes(nof_args=2, kwargs_names=["what", "key"])
def encrypt_with_key(what, key):
    return encrypt_with_box(what, craft_secret_box(key))


@enforce_bytes(kwargs_names="what")
def encrypt_with_password(what, password):
    key = craft_key_from_password(password)
    return encrypt_with_key(what, key), key


@safe_decryption
@enforce_bytes(kwargs_names="what")
def decrypt_with_box(what, secret_box):
    return secret_box.decrypt(what)


@enforce_bytes(kwargs_names="what")
def decrypt_with_key(what, key):
    return decrypt_with_box(what, craft_secret_box(key))


def encrypt_note(note, password=None):
    password = (password or "").encode() or generate_random_chars()

    ciphertext, key = encrypt_with_password(note, password)

    # needs to be url safe so we can share it around
    return map(url_safe_encode, (ciphertext, key))


def encrypt_note_with_params(note, password, algorithm, hardness):
    key = craft_key_from_password(password,
                                  craft_kdf_params(algorithm, hardness))
    ciphertext = encrypt_with_key(note, key)

    # needs to be url safe so we can share it around
    return map(url_safe_encode, (ciphertext, key))


@safe_decryption
def decrypt_note(payload, key):
    return decrypt_with_key(*map(url_safe_decode, (payload, key)))


def benchmark_algorithms():
    def measure(*args):
        return timeit.timeit("crypto.craft_key_from_password('lalal', "
                             "crypto.craft_kdf_params('{0}', '{1}'))"
                             .format(*args),
                             setup="from cenotes_lib import crypto", number=1)

    algorithm_combinations = (pair for combinations in
                              (product([x[0]], x[1].get("hardness").keys())
                               for x in SUPPORTED_ALGORITHM_PARAMS.items())
                              for pair in combinations)
    return map(lambda x: (x, measure(*x)), algorithm_combinations)
