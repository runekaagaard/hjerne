.PHONY: aider list-files

aider:
	find . -type f -not -path '*/\.git/*' | grep -v -f .exclude | xargs aider

list-files:
	find . -type f -not -path '*/\.git/*' | grep -v -f .exclude
