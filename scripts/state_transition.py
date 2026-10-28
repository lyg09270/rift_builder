"""A snapshot-bound affine transition: [next_state, 1] = matrix @ [state, 1]."""

from dataclasses import dataclass

import numpy as np

from game_state import STATE_FIELDS, STATE_SIZE, game_state


class TransitionError(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


@dataclass(frozen=True)
class StateTransition:
    label: str
    matrix: np.ndarray
    reference: np.ndarray
    target_after: object = None

    def __post_init__(self):
        matrix = np.array(self.matrix, dtype=np.float64, copy=True)
        reference = game_state(self.reference).to_vector()
        if matrix.shape != (STATE_SIZE + 1, STATE_SIZE + 1) or not np.isfinite(matrix).all():
            raise ValueError("Invalid affine transition matrix")
        if not np.array_equal(matrix[-1], np.eye(STATE_SIZE + 1)[-1]):
            raise ValueError("The homogeneous coordinate must remain 1")
        matrix.setflags(write=False)
        reference.setflags(write=False)
        object.__setattr__(self, "matrix", matrix)
        object.__setattr__(self, "reference", reference)

    @classmethod
    def between(cls, label, before: game_state, after: game_state, target_after=None):
        before.validate()
        after.validate()
        matrix = np.eye(STATE_SIZE + 1)
        matrix[:-1, -1] = after.vector - before.vector
        return cls(label, matrix, before.vector, target_after)

    def apply(self, state: game_state) -> game_state:
        state.validate()
        if not np.array_equal(state.vector, self.reference):
            raise TransitionError("stale_matrix", "Rebind the card to the changed state before applying its matrix")
        result = self.matrix @ np.append(state.vector, 1.0)
        return game_state(result[:-1])

    def then(self, following):
        intermediate = self.apply(game_state(self.reference))
        if not np.array_equal(intermediate.vector, following.reference):
            raise TransitionError("incompatible_sequence", "The next matrix must be bound to this transition's result")
        return type(self)(f"{self.label}; {following.label}", following.matrix @ self.matrix,
                          self.reference, following.target_after)

    def changes(self) -> dict[str, float]:
        after = self.apply(game_state(self.reference))
        delta = after.vector - self.reference
        return {index.name: float(delta[index]) for index in STATE_FIELDS if delta[index] != 0}
