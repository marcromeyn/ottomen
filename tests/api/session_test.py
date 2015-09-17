from . import OttomenApiTestCase


class SessionApiTestCase(OttomenApiTestCase):
    def test_test(self):
        r = self.send_get_request('/session/test')
        db_session = self.db_session()

        self.assertOkJson(r)

    def test_start_missing_task_id(self):
        to_send = {
            "session": {
                "turk_id": "12345"
            }
        }
        r = self.send_post_request('/session/', to_send)

        self.assertStatusCode(r, 400)

    def test_start_missing_turk_id(self):
        to_send = {
            "session": {
                "task_id": "12345"
            }
        }
        r = self.send_post_request('/session/', to_send)

        self.assertStatusCode(r, 400)
