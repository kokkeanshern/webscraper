from pathlib import Path


class Captcha:
    base_dir = Path(__name__).resolve().parent / "images"

    raw_image_file = base_dir / "captcha_raw.png"
    bnw_image_file = base_dir / "captcha_bw.png"
    first_threshold_file = base_dir / "captcha_first_threshold.png"
    blurred_image_file = base_dir / "captcha_blurred.png"
    final_image_file = base_dir / "captcha_final.png"


class Links:
    fundaztic_login = "https://p2p.fundaztic.com/visitor/to-login"
    fundaztic_transaction_download = (
        "https://p2p.fundaztic.com/depositshistory/init_eight_export"
    )


class FundazticLocators:
    login_page__email_input = "username"
    login_page__password_input = "pwd"
    login_page__captcha_input = "captcha"
    login_page__captcha_puzzle = "img[src*='/cic/code?name=user_login']"


class ApiParams:
    def __init__(self, initial=None):
        self.params = dict(initial) if initial else {}

    def add(self, key: str, value: str = None):
        self.params[key] = value

    def update(self, data: dict):
        self.params.update(data)
