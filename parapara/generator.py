# --------------------------------------------------------
# 結果描画用のモジュールや関数
# https://qiita.com/Mikaner/items/0fe55d4f0f3b4848cad6
# --------------------------------------------------------
import io
import os
from IPython.display import HTML

# なくても動いた
# from JSAnimation.IPython_display import display_animation

import matplotlib
from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np
from pyvirtualdisplay import Display


display = Display(visible=0, size=(1024, 768))
display.start()
os.environ["DISPLAY"] = f":{display.display}"


def _make_anim(frames: np.ndarray) -> animation.FuncAnimation:
    plt.figure(figsize=(frames[0].shape[1] / 72.0, frames[0].shape[0] / 72.0), dpi=72)
    patch: matplotlib.image.AxesImage = plt.imshow(frames[0])
    plt.axis("off")

    def animate(i: int) -> None:
        patch.set_data(frames[i])

    anim: animation.FuncAnimation = animation.FuncAnimation(
        plt.gcf(), animate, frames=len(frames), interval=50
    )
    return anim


def play_anim(frames: list[np.ndarray]) -> HTML:
    """
    Convert a series of numpy-array-images into an animation for displaying on jupyter notebook

    np.ndarray 型で表現された複数の画像を、jupyter notebook で描画可能な一連のアニメーションへと変換する
    """
    jshtml: str = _make_anim(frames).to_jshtml()
    return HTML(jshtml)


def save_as_gif(frames: list[np.ndarray], filename: str) -> str:
    """
    Save a list of frames as a gif
    """

    anim: animation.FuncAnimation = _make_anim(frames)
    anim.save(filename + ".gif")
    return anim.to_jshtml()


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
