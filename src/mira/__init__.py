from subprocess import run

from ._generated import (
    Question,
    Claim,
    Evidence,
    Study,
    Protocol,
    Request,
)

__all__ = [
    "Question",
    "Claim",
    "Evidence",
    "Study",
    "Protocol",
    "Request",
]


def main():
    run(["make"])
