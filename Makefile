.PHONY: help lint_checker play_tictactoe play_connect4 play_othello

help: ## show this help
	@grep -E '^[a-zA-Z_-][a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

lint_checker: ## Run lint checker on source files
	pyright bin/**/*.py src/**/*.py

######################################################

play_tictactoe:	## Play Tic Tac Toe
	python3 bin/play_game.py --game tictactoe

play_connect4:	## Play Connect 4
	python3 bin/play_game.py --game connect4

play_othello:	## Play Othello
	python3 bin/play_game.py --game othello

