VENV = .venv
PYTHON = $(VENV)/bin/python

serve: install
	bundle exec jekyll serve --livereload --host localhost

install:
	bundle install

build: install
	bundle exec jekyll build

check_links: build
	bundle exec htmlproofer --ignore_missing_alt true --ignore_empty_alt true --ignore_status_code "0,403,503" ./_site

$(VENV):
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install Pillow pyyaml

resize_student_images: $(VENV)
	$(PYTHON) resize_student_images.py

delete_old_student_images: $(VENV)
	$(PYTHON) delete_old_student_images.py

