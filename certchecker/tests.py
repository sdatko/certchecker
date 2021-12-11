#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import tempfile
import unittest
from unittest.mock import mock_open
from unittest.mock import patch

from certchecker.expiration import get_cert_expiration_from_file
from certchecker.expiration import get_cert_expiration_from_host
from certchecker.expiration import get_days_to_expiration


TEST_CERT = '''-----BEGIN CERTIFICATE-----
MIIFiTCCA3GgAwIBAgIUQYYXOXTrUPFkebRiaox9cKKqwZQwDQYJKoZIhvcNAQEL
BQAwVDELMAkGA1UEBhMCUEwxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDENMAsGA1UEAwwEdGVzdDAeFw0yMTEy
MTIyMzM4NDVaFw0yMjEyMTIyMzM4NDVaMFQxCzAJBgNVBAYTAlBMMRMwEQYDVQQI
DApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQx
DTALBgNVBAMMBHRlc3QwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDG
2d8pHAkVIMQ2JzwQ6/C4ZDSucDx5XxNLGYazEXQgkoKK3C+pr4E9TJGy5RRG40w1
lJQp2jIkGeFQoQjoVObf/eD0KnJebG1DLYUtk5riPJCy+JHcD25RZGO2L53i0bck
t2mqKdvLFgUzF226mpU2tDJWL9OupDNIiR7NRJFCJXIcOvPYqrIqy6UtQtEFgj5R
/RCzUjPAzavWAsTZbYjExV61jD0yiYBU/iOpbujP5eF3JRQmTs4ufesYPzLVj66X
dLUaHhgpw92Fk8jszFngnZ6xzNDLn8kL4gbhJYm3Yib53vSZ5eVEuVvZwYB04XFE
mAfpLj+yYhPTsrj6HD/znaqvt/CDPFmOtl30XeegApBFAwQJIzA15omTiR1Tbp5/
8V7giEkoMlcaP6xfPDH2FVU84OLLIWcURK6TKMDuGMrIytedMh1ylkM8WzSR+jKO
0Qd3zhOxCyYXzHfjXcnrBMCxcp7GzIu9UBmEaeopID02ApyXQdvGpfH27HKzgIpm
aApANvYEfF473/7Pi7WYvYdZdE2QmLzR2Wry6mTfXxgKsKvXqtIhki7cjL6Agtco
c1VyssIdAfaGo5m4MIi5r3dC7FeU81LnOFVZ9q9YQ+hL2eeEdolppCCBYaVmIcLc
6DerRo1JtYddEc9BhajSgo+TLKJYHgVz/8jFLyxTYwIDAQABo1MwUTAdBgNVHQ4E
FgQUL6sOzjI0XZocpKSe7S+KUJkdVjgwHwYDVR0jBBgwFoAUL6sOzjI0XZocpKSe
7S+KUJkdVjgwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAgEATWBE
3rRqghsBzQpyS+0wXOFtCrBOGp9BUzCUAgcBEteoDxDUDwg+6Mphg/Dg6jxYr8wm
IYHYdxhBfydOBFmPpiwVYkVnOOLrlagfp/YIorNVFlv9hQhIm9+3EsvXUrDplnRM
+p2O+V9h0uWDKNl2rrywwGqKquS3bVY7WPJOkAQYPF4SAxODrnmzP7SB0WIPz9BY
vdCx3GgT4Y/DmOgR6GdKhrEWarcNdNq5DSj5aMZQZR0W2zhpbpvPvxTppXSLsMi7
mSdPLf71g9J64nZngRS09N4CdVJeP3JA6jY3JMbcEiBm2FqbLk+dzEasxjW1Nwpa
zFoRVCwN1BtpfQxfgZ/crawlUsNEKLHn6W4dDe1/zLA24zOBwAfGZ/s+nEsLmo6N
eK4ZVSAtzd9/BTjnNmgPpDZzfMpH0QkYDnEJVh79kpqyZPwl5vWcWs8kpVdUZ0nE
dd4HaWtWuL9mr+Q6uGQ0Nwz04EzhtmoEmLkGHzrIn8icBilEw71JeHv6LgNwtJRa
I1MPCCzGKYe8YSlgO6IJX5/Izld4wv0umA9y6WRKs4VVEhxLmBv5smaBTJ7qSBx5
hUL9g/0c5Z8pp447F+bypJE7CQJAFTB2lkIu0mugL6lL9F/BZqeqrCQjlV5ETYNi
TdrNUNobHgrem6q3gvEC7YXOcgC0VFd4ra3SCRk=
-----END CERTIFICATE-----'''


class TestCertChecker(unittest.TestCase):
    def test_get_cert_expiration_from_host(self):
        mock1 = 'certchecker.expiration.request.socket.create_connection'
        mock2 = 'certchecker.expiration.request.ssl.SSLContext.wrap_socket'

        with patch(mock1) as sock_mock:
            sock_mock.return_value.__enter__.return_value = None

            with patch(mock2) as ssock_mock:
                ssock_mock.return_value.\
                    __enter__.return_value\
                    .getpeercert.return_value = {
                        'notAfter': 'Dec 12 23:38:45 2022 GMT'
                    }

                actual_datetime = get_cert_expiration_from_host('test', 443)

        expected_datetime = datetime.strptime('2022-12-12 23:38:45',
                                              '%Y-%m-%d %H:%M:%S')

        assert actual_datetime == expected_datetime

    def test_get_cert_expiration_from_file(self):
        with patch('certchecker.expiration.open',
                   mock_open(read_data=bytes(TEST_CERT, encoding='UTF-8'))):
            actual_datetime = get_cert_expiration_from_file('test')

        expected_datetime = datetime.strptime('2022-12-12 23:38:45',
                                              '%Y-%m-%d %H:%M:%S')

        assert actual_datetime == expected_datetime

    def test_get_cert_expiration_from_file_2(self):
        with tempfile.NamedTemporaryFile() as cert_file:
            cert_file.write(bytes(TEST_CERT, encoding='UTF-8'))
            cert_file.seek(0)
            actual_datetime = get_cert_expiration_from_file(cert_file.name)

        expected_datetime = datetime.strptime('2022-12-12 23:38:45',
                                              '%Y-%m-%d %H:%M:%S')

        assert actual_datetime == expected_datetime

    def test_get_days_to_expiration(self):
        date1 = datetime.now() + timedelta(hours=1)
        date2 = datetime.now() + timedelta(days=7, hours=1)
        date3 = datetime.now() - timedelta(days=12, hours=6)

        difference = get_days_to_expiration(date1)
        self.assertEqual(difference, 0)

        difference = get_days_to_expiration(date2)
        self.assertEqual(difference, 7)

        difference = get_days_to_expiration(date3)
        self.assertEqual(difference, -13)


if __name__ == '__main__':
    unittest.main(verbosity=2)
