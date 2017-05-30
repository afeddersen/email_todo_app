##########################################################################
#
# This is a simple menu system to manage the GAE deployment of Convoy
# This script makes use of termcolor which adds color to the terminal output
# To install: pip install termcolor
#
##########################################################################

import subprocess
import sys
from termcolor import colored

# commands to push to staging
deploy_staging_index = 'yes Y 2>/dev/null | gcloud app deploy --project a1977fed --no-promote --version staging index.yaml'
deploy_staging_cron = 'yes Y 2>/dev/null | gcloud app deploy --project a1977fed --no-promote --version staging cron.yaml'
deploy_staging_push = 'yes Y 2>/dev/null | gcloud app deploy --project a1977fed --no-promote --version staging app.yaml'

# commands to push to production
deploy_prod_index = 'yes Y 2>/dev/null | gcloud app deploy --project a1977fed --version 1 index.yaml'
deploy_prod_cron = 'yes Y 2>/dev/null | gcloud app deploy --project a1977fed --version 1 cron.yaml'
deploy_prod_push = 'yes Y 2>/dev/null | gcloud app deploy --project a1977fed --version 1 app.yaml'


def staging_one():
    print colored('pushing index.yaml to staging...', 'green')
    subprocess.call(deploy_staging_index, shell=True)


def staging_two():
    print colored('pushing cron.yaml to staging...', 'green')
    subprocess.call(deploy_staging_cron, shell=True)


def staging_three():
    print colored('pushing new version to staging...', 'green')
    subprocess.call(deploy_staging_push, shell=True)


def option_two():
    print colored('Pushing to prod...', 'green')
    #subprocess.call(deploy_prod_index, shell=True)
    #subprocess.call(deploy_prod_cron, shell=True)
    subprocess.call(deploy_prod_push, shell=True)


subprocess.call('clear')

print '''
Convoy deployment tool

Choose an option:

1. Push to staging

* Deploy a new index.yaml file to staging
* Deploy a new cron.yaml file to staging
* Deploy the Convoy application to staging

2. Push to production

* Deploy a new index.yaml file to prod
* Deploy a new cron.yaml file to prod
* Deploy the Convoy application to prod

Press enter to quit

'''

while True:
    answer = raw_input('What option do you choose? ')

    if answer == '':
        sys.exit()

    elif answer == '1':
        staging_one()
        staging_two()
        staging_three()
        sys.exit()

    elif answer == '2':
        option_two()
        sys.exit()

    else:
        print colored('Not a valid choice!', 'red')
