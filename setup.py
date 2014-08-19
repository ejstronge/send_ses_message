from setuptools import setup

setup(
    name='send_ses_message',
    version='0.1rc1',
    packages=['send_ses_message'],
    scripts=['ses_smtp_mailer.py'],
    license='MIT',

    package_data={
        'send_ses_message': ['examples/*.cfg'],
    },
    author='Edward J. Stronge',
    author_email='ejstronge@gmail.com',
    description='Send email using the Amazon SES IMAP interface',
    keywords='aws ses email',
    long_description=open('./README.md').read(),
)
