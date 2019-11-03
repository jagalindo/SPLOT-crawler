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
	git add ./downloads/*
	git push --quiet https://${GH_TOKEN}@github.com/jagalindo/SPLOT-crawler.git
}

setup_git
commit_website_files
upload_files

