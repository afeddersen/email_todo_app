# Shell script to start a local App Engine development server
#
# Script begins by updating gcloud CLI
#
# This version of the script blows away the local datastore
#
# https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server

gcloud components update

dev_appserver.py --clear_datastore=yes --log_level=debug app.yaml
