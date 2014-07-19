
# Send SES Email

## Edward Stronge <ejstronge@gmail.com>

Send debugging messages from Amazon EC2 instances.

# Usage

* Read email contents from a text stream: Requires an `smtp_credentials.cfg` file;
  run `ses_smtp_mailer --help` for details.

```bash
echo "Useful debugging information" | \
    ses_smtp_mailer -s "Processing results" -f me@example.com user@example
```

* Use module from another Python script. Your calling script should catch
  smtplib.SMTPException exceptions and retry message sending as needed.

```python
from send_smtp_ses_email import get_smtp_parameters, get_server_reference

smtp_params = get_smtp_parameters('parameters_file.cfg')
smtp_con = get_server_reference(*smtp_params)

smtp_con.sendmail('me@example.com', 'you@example.com',
                  """From: me@example.com\r\n
                     To: you@example.com\r\n

                     %s
                  """ % 'interesting text')
```

# Forthcoming

* Send email from a `logging` handler

(c) 2014 Edward J. Stronge. Available under the MIT License; see LICENSE.
