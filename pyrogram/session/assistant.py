import base64
from pyrogram.session import Session

class StringSession(Session):
    def __init__(self, string=None):
        if string:
            dc_id, auth_key, test_mode = self.decode(string)
            super().__init__(None, dc_id, auth_key, test_mode)
        else:
            super().__init__(None, 0, b"", False)

    @staticmethod
    def encode(dc_id, auth_key, test_mode):
        return base64.urlsafe_b64encode(
            b"".join(
                (
                    dc_id.to_bytes(1, "little"),
                    test_mode.to_bytes(1, "little"),
                    auth_key
                )
            )
        ).decode().rstrip("=")

    @staticmethod
    def decode(string):
        data = base64.urlsafe_b64decode(string + "=" * (4 - len(string) % 4))
        dc_id = data[0]
        test_mode = data[1]
        auth_key = data[2:]
        return dc_id, auth_key, test_mode
