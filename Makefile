.PHONY: aider list-files

aider:
	find . -type f | grep -v -f .exclude | xargs aider

list-files:
	find . -type f | grep -v -f .exclude
