from __future__ import print_function

import dataclasses


@dataclasses.dataclass
class TraktorMetadata:
    current_track_deck_a = "N/A"
    current_track_elapsed_deck_a = 0

    current_track_deck_b = "N/A"
    current_track_elapsed_deck_b = 0

    master_deck = "N/A"