import pytest

from game import COUNT_TRIES, Game, GameOverError, InvalidMoveError
from checker import ABSENT, CORRECT, PRESENT

ALLOWED = {"apple", "crane", "plane"}


def make_game():
    return Game("apple", ALLOWED)


def test_win_ends_game():
    game = make_game()
    game.make_guess("crane")
    assert not game.is_win()
    assert not game.is_over()

    game.make_guess("apple")
    assert game.is_win()
    assert game.is_over()

    # после победы ходить нельзя
    with pytest.raises(GameOverError):
        game.make_guess("plane")


def test_invalid_guess_does_not_spend_attempt():
    game = make_game()
    for bad_word in ["zzzzz", "app", "ap1le"]:
        with pytest.raises(InvalidMoveError):
            game.make_guess(bad_word)

    assert game.attempts_left == COUNT_TRIES
    assert game.attempts == []


def test_loss_after_all_attempts_used():
    game = make_game()
    for _ in range(COUNT_TRIES):
        game.make_guess("crane")

    assert game.is_over()
    assert not game.is_win()
    with pytest.raises(GameOverError):
        game.make_guess("crane")

def test_letter_states_keep_best_status():
    game = Game("apple", {"ppppp", "crane"})
    game.make_guess("ppppp")
    game.make_guess("crane")
    states = game.letter_states
    assert states["p"] == CORRECT
    assert states["a"] == PRESENT
    assert states["c"] == ABSENT
    assert "z" not in states