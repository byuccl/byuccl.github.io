serve: install
	bundle exec jekyll serve --livereload

install:
	bundle install

build: install
	bundle exec jekyll build

check_links: build
	bundle exec htmlproofer --ignore_missing_alt true --ignore_empty_alt true --ignore_status_code "0,403" ./_site

