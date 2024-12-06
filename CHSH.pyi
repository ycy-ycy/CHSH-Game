from typing import List

class Game:
    """
    Represents a single CHSH game.

    Attributes:
        x: Alice's input (0 or 1).
        y: Bob's input (0 or 1).
        a: Alice's output (0 or 1).
        b: Bob's output (0 or 1).
    """
    x: bool
    y: bool
    a: bool
    b: bool

class GameResult:
    """
    Represents the result of the CHSH game analysis.

    Attributes:
        n00, n01, n10, n11: Counts of games with different (x, y) pairs.
        w00, w01, w10, w11: Counts of wins for different (x, y) pairs.
        WinRate00, WinRate01, WinRate10, WinRate11: Win rates for each (x, y) pair.
        n: Total number of games.
        w: Total number of wins.
        WinRate: Overall win rate.
    """
    n00: int
    n01: int
    n10: int
    n11: int
    w00: int
    w01: int
    w10: int
    w11: int
    WinRate00: float
    WinRate01: float
    WinRate10: float
    WinRate11: float
    n: int
    w: int
    WinRate: float

    def __repr__(self) -> str: 
        """Return a string representation of the Game object."""
        ...

def PlayRandom(n: int) -> List[Game]:
    """
    Simulate random games and return a list of results.

    Args:
        n: Number of games to simulate.

    Returns:
        A list of Game objects.
    """
    ...

def PlayClassical(
    n: int,
    Strategy: bool = False
) -> List[Game]:
    """
    Simulate classical version games and return a list of results.

    Args:
        n: Number of games to simulate.
        Strategy: Alice and Bob will both give Strategy as return (default: False).
    
    Returns:
        A list of Game objects.
    """
    ...

def PlayQuantum(
    n: int,
    err: float,
    diff_a: float,
    diff_0: float,
    diff_b: float,
    Alice_first: bool = True
) -> List[Game]:
    """
    Simulate quantum version games and return a list of results.

    Args:
        n: Number of games to simulate.
        err: Error rate of the entangled state.
        diff_a: Difference for Alice.
        diff_0: Base difference between Alice and Bob.
        diff_b: Difference for Bob.
        Alice_first: Whether Alice moves first (default: True).
    
    Returns:
        A list of Game objects.
    """
    ...

def Analyze(games: List[Game]) -> GameResult:
    """
    Analyze a list of games and return a summary.

    Args:
        games: A list of Game objects.

    Returns:
        A GameResult object summarizing the analysis.
    """
    ...
