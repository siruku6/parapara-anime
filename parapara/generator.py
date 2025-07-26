# --------------------------------------------------------
# 結果描画用のモジュールや関数
# https://qiita.com/Mikaner/items/0fe55d4f0f3b4848cad6
# --------------------------------------------------------
import io
import os
from typing import Optional

# なくても動いた
# from JSAnimation.IPython_display import display_animation
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
from matplotlib import animation
from pyvirtualdisplay import Display

from parapara.components.progress_display import ProgressDisplay
from parapara.components.validation import check_package_existence

display = Display(visible=0, size=(1024, 768))
display.start()
os.environ["DISPLAY"] = f":{display.display}"


def _make_anim(frames: np.ndarray, interval: int) -> animation.FuncAnimation:
    """
    Convert a series of numpy-array-images into an animation
    np.ndarray 型で表現された複数の画像を、アニメーションへと変換する

    Parameters
    ------
    frames: list[np.ndarray]
        List of numpy-array-images
    interval: int
        Interval between frames in milliseconds

    Returns
    ------
    anim: matplotlib.animation.FuncAnimation
        Animation object
    """

    plt.figure(figsize=(frames[0].shape[1] / 72.0, frames[0].shape[0] / 72.0), dpi=72)
    patch: matplotlib.image.AxesImage = plt.imshow(frames[0])
    plt.axis("off")

    def animate(i: int) -> None:
        patch.set_data(frames[i])

    anim: animation.FuncAnimation = animation.FuncAnimation(
        plt.gcf(), animate, frames=len(frames), interval=interval
    )

    # This suppresses the display figure on the notebook
    plt.close()

    return anim


def play_anim(frames: list[np.ndarray], interval: int = 50) -> HTML:
    """
    Convert a series of numpy-array-images into an animation for displaying on jupyter notebook
    np.ndarray 型で表現された複数の画像を、jupyter notebook で描画可能な一連のアニメーションへと変換する

    Parameters
    ------
    frames: list[np.ndarray]
        List of numpy-array-images
    interval: int
        Interval between frames in milliseconds

    Returns
    ------
    HTML
        Animation object
    """
    jshtml: str = _make_anim(frames, interval).to_jshtml()
    return HTML(jshtml)


def _save(
    frames: list[np.ndarray],
    filename: str,
    extension: str,
    interval: int = 50,
    fps: int = 30,
    save_dir: Optional[str] = None,
) -> bool:
    """
    Returns
    ------
    bool
        True if the saving was successful, False otherwise
    """
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # プログレスバーのコールバック関数を取得
    prog_disp: ProgressDisplay = ProgressDisplay(n_frames=len(frames))
    progress_callback = prog_disp.progress_callback

    save_path: str = os.path.join(save_dir, filename) if save_dir else filename
    save_path += f".{extension}"

    anim: animation.FuncAnimation = _make_anim(frames, interval=interval)

    if extension == "gif":
        writer: str = "pillow"
        fps = None  # type: ignore
    elif extension == "mp4":
        writer = "ffmpeg"
    else:
        print("[ERROR] Unsupported file format. Use 'gif' or 'mp4'.")
        return False

    anim.save(save_path, writer=writer, fps=fps, progress_callback=progress_callback)
    print("[INFO] Animation is saved as", save_path)
    return True


def save_as_gif(
    frames: list[np.ndarray],
    filename: str,
    interval: int = 50,
    save_dir: Optional[str] = None,
) -> None:
    """
    Save a list of frames as a gif
    np.ndarray 型で表現された複数の画像を、GIF 形式で保存する

    Parameters
    ------
    frames: list[np.ndarray]
        List of numpy-array-images
    filename: str
        Filename to save the gif (without extension !)
    interval: int
        Interval between frames in milliseconds

    Returns
    ------
    None
    """

    result: bool = _save(
        frames,
        filename,
        extension="gif",
        interval=interval,
        save_dir=save_dir,
    )


def save_as_mp4(
    frames: list[np.ndarray],
    filename: str,
    fps: int = 20,
    save_dir: Optional[str] = None,
) -> None:
    """
    Save a list of frames as a mp4
    np.ndarray 型で表現された複数の画像を、MP4 形式で保存する

    Parameters
    ------
    frames: list[np.ndarray]
        List of numpy-array-images
    filename: str
        Filename to save the mp4 (without extension !)
    fps: int
        Frames per second for the video

    Returns
    ------
    None
    """
    check_package_existence("ffmpeg")

    result: bool = _save(
        frames,
        filename,
        extension="mp4",
        fps=fps,
        save_dir=save_dir,
    )


def to_numpy(fig: plt.Figure) -> np.ndarray:
    """
    Convert Figure into numpy array

    Parameters
    ------
    fig: matplotlib.pyplot.Figure
        Figure which you want to convert into numpy array

    References
    ------
    https://pystyle.info/matplotlib-convert-figure-to-bytes-and-base64/
    https://stackoverflow.com/a/61443397/8674852
    https://jun-networks.hatenablog.com/entry/2019/11/01/020536
    """
    # インメモリのバイナリストリームを作成
    io_buf = io.BytesIO()

    # matplotlibから出力される画像のバイナリデータをメモリに格納
    fig.savefig(io_buf, format="raw")

    # ストリーム位置を先頭に戻る
    io_buf.seek(0)

    new_shape = (int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1)
    # メモリからバイナリデータを読み込み, numpy array 形式に変換
    img_arr: np.ndarray = np.frombuffer(io_buf.getvalue(), dtype=np.uint8).reshape(
        new_shape
    )

    io_buf.close()
    return img_arr
