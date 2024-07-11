.PHONY: aider list-files

aider:
	find . -type f -not -path '*/\.git/*' $(shell sed 's/^/-not -path "*/' .exclude | sed 's/$$/*"/' | tr '\n' ' ') | xargs aider

list-files:
	find . -type f -not -path '*/\.git/*' $(shell sed 's/^/-not -path "*/' .exclude | sed 's/$$/*"/' | tr '\n' ' ')
