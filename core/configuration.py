from dataclasses import dataclass
@dataclass(frozen=True)
class ReviewPolicy:
    block_on_medium: bool = False
    offline_mode: bool = True
DEFAULT_POLICY = ReviewPolicy()
