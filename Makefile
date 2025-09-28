.PHONY: help lint_checker play_tictactoe play_connect4 play_othello

help: ## show this help
	@grep -E '^[a-zA-Z_-][a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

lint_checker: ## Run lint checker on source files
	pyright bin/**/*.py src/**/*.py

test: lint_checker test_all_games ## Run all tests

profile:	## Profile AI vs AI simulations for Connect 4
	python -m cProfile -s time ./bin/play_game.py -f ai -s ai -sim 500 -g connect4

######################################################

play_tictactoe:	## Play Tic Tac Toe
	./bin/play_game.py --game tictactoe

play_connect4:	## Play Connect 4
	./bin/play_game.py --game connect4

play_othello:	## Play Othello
	./bin/play_game.py --game othello

#######################################################

test_tictactoe: ## Run AI vs AI simulations for Tic Tac Toe
	./bin/play_game.py --game tictactoe -f ai -s ai -gpm 5 -sim 5 --seed 123

test_connect4: ## Run AI vs AI simulations for Connect 4
	./bin/play_game.py --game connect4 -f ai -s ai -gpm 5 -sim 5 --seed 123

test_othello: ## Run AI vs AI simulations for Othello
	./bin/play_game.py --game othello -f ai -s ai -gpm 5 -sim 5 --seed 123

test_all_games: test_tictactoe test_connect4 test_othello ## Run AI vs AI simulations for all games
