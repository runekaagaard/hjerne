.PHONY: aider

aider:
	find . -type f | grep -v -f .exclude | xargs aider
