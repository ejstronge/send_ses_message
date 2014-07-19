# -*- coding: utf-8 -*-
"""
   send_ses_email.py
   =================

   Send email messages using the AWS SES. Credentials are loaded from a
   configuration file.

   (c) 2014, Edward J. Stronge Available under the MIT License - see LICENSE
   for details.
"""
import argparse
import ConfigParser
from email.mime.text import MIMEText
import smtplib
import sys
import time

# XXX do need to allow outbound traffic to use this?

# need to have retry logic in sending to amazon


def get_server_reference(
        username, smtp_password, aws_smtp_endpoint, aws_smtp_port):
    """
       Returns smtplib.smtp reference using the specified parameters.
       Call sendmail on the returned reference to send emails.

       See the example configuration file for explanations on where to
       find these parameters.
    """
    smtp_con = smtplib.SMTP(
        host=aws_smtp_endpoint, port=aws_smtp_port, timeout=10)
    smtp_con.starttls()
    smtp_con.ehlo()
    smtp_con.login(username, smtp_password)
    # Will need to re-obtain this reference occasionally as server
    # connections aren't maintained long-term
    return smtp_con


def get_smtp_parameters(config_file_sequence):
    """
       Read the configuration files in config_file_sequence
       and return a dictionary of the parameter specified
       in their 'default' section.
    """
    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read(config_file_sequence)
    return {i[0].lower(): i[1] for i in config_parser.items('default')}


def main():
    """
       Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Simple email tool backed by the Amazon SES SMTP interface")
    parser.add_argument('-s', '--subject', help="Subject of email")
    parser.add_argument('-f', '--from_email', help="Email sender")
    parser.add_argument(
        '--config_file', default='smtp_credentials.cfg',
        help="CFG file of SMTP user credentials. Must define variables"
             "USERNAME, SMTP_PASSWORD, AWS_SMTP_ENDPOINT, and AWS_SMTP_PORT"
             "in a 'default' section.")
    parser.add_argument('to_email', help="Email recipient")
    parser.add_argument(
        'message', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help="File containing email text. By default, reads text from stdin")

    args = parser.parse_args()
    configuration_params = get_smtp_parameters([args.config_file])

    message = MIMEText(args.message.read())
    message['Subject'] = args.subject
    message['From'] = args.from_email
    message['To'] = args.to_email
    try:
        server = get_server_reference(*configuration_params)
        server.sendmail(args.from_email, args.to_email, message.as_string())
    except smtplib.SMTPException:
        server.quit()
        time.sleep(30)
        server = get_server_reference(*configuration_params)
        server.sendmail(args.from_email, args.to_email, message.as_string())
    finally:
        server.quit()


if __name__ == '__main__':
    main()
