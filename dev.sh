# Shell script to start a local App Engine development server
#
# Script begins by updating gcloud CLI
#
# https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server

gcloud components update

dev_appserver.py --log_level=debug app.yaml
