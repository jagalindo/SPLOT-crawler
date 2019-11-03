#!/bin/sh

setup_git() {
  git config --global user.email "jagalindo@us.es"
  git config --global user.name "Travis CI"
}

commit_website_files() {
  git add ./downloads/*
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
	git remote add origin-master https://${GH_TOKEN}@github.com/jagalindo/SPLOT-crawler.git > /dev/null 2>&1
	git push --quiet --set-upstream origin-master master
}

setup_git
commit_website_files
upload_files

