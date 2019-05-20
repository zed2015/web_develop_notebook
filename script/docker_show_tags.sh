#!/bin/sh
#
# Simple script that will display Docker repository tags
# using basic tools: curl, sed, grep, and sort.
#
# Usage:
#   $ docker-show-repo-tags.sh ubuntu centos
for Repo in $* ; do
    curl -sS "https://hub.docker.com/r/library/$Repo/tags/" | \
        sed -e $'s/"tags":/\\\n"tags":/g' -e $'s/\]/\\\n\]/g' | \
        grep '^"tags"' | \
        grep '"library"' | \
        sed -e $'s/,/,\\\n/g' -e 's/,//g' -e 's/"//g' | \
        grep -v 'library:' | \
        sort -fu | \
        sed -e "s/^/${Repo}:/"
done
