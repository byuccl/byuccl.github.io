serve:
	bundle exec jekyll serve

build:
	bundle exec jekyll build

check_links: build
	bundle exec htmlproofer --empty_alt_ignore --url-ignore "/www.mouser.com/" ./_site

