from flask import Flask, send_from_directory, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
import os
import argparse

app = Flask(__name__)
auth = HTTPBasicAuth()

BASE_DIR = os.path.abspath("./")

PASSWORD_HASH = None
REQUIRE_PASSWORD = True


@auth.verify_password
def verify(username, password):
    if not REQUIRE_PASSWORD:
        return True
    return PASSWORD_HASH and check_password_hash(PASSWORD_HASH, password)


@app.route("/<path:filename>")
@auth.login_required
def files(filename):
    real_path = os.path.realpath(os.path.join(BASE_DIR, filename))
    if not real_path.startswith(BASE_DIR + os.sep):
        abort(403)
    return send_from_directory(BASE_DIR, filename)


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="CLIServer",
        description="Local CLI WAN file server for wget"
    )
    parser.add_argument(
        "--no-password", "-no",
        action="store_true",
        help="Disable authentication entirely"
    )
    parser.add_argument(
        "--password","-ps",
        default="dingus",
        help="Password required to access files"
    )
    parser.add_argument(
        "--port","-po",
        default=8888,
        help="Port to run the server on"
    )
    return parser


def main():
    global PASSWORD_HASH, REQUIRE_PASSWORD

    args = init_parser().parse_args()

    REQUIRE_PASSWORD = not args.no_password

    if REQUIRE_PASSWORD:
        PASSWORD_HASH = generate_password_hash(args.password)
        print("Authentication ENABLED")
    else:
        print("Authentication DISABLED")

    app.run(host="0.0.0.0", port=int(args.port))


if __name__ == "__main__":
    main()
