from typing import Callable

from tqdm.auto import tqdm


# tqdm のインスタンスを手動で作成
class ProgressDisplay:
    def __init__(self, n_frames: int) -> None:
        self.progress_bar: tqdm = tqdm(
            total=n_frames, desc="Saving frames...", unit="frame"
        )

    def _progress_callback(self, current_frame: int, total_frames: int) -> None:
        self.progress_bar.update(current_frame + 1 - self.progress_bar.n)
        if current_frame + 1 == total_frames:
            self.progress_bar.close()

    @property
    def progress_callback(self) -> Callable[[int, int], None]:
        """
        Returns a callback function that updates the progress bar.
        """
        return self._progress_callback
