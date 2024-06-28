# --------------------------------------------------------
# 結果描画用のモジュールや関数
# https://qiita.com/Mikaner/items/0fe55d4f0f3b4848cad6
# --------------------------------------------------------
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


def make_anim(frames: np.ndarray) -> animation.FuncAnimation:
    plt.figure(
        figsize=(frames[0].shape[1] / 72.0, frames[0].shape[0] / 72.0), dpi=72
    )
    patch: matplotlib.image.AxesImage = plt.imshow(frames[0])
    plt.axis('off')

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
    jshtml: str = make_anim(frames).to_jshtml()
    return HTML(jshtml)


def save_as_gif(frames: list[np.ndarray], filename: str) -> str:
    """
    Save a list of frames as a gif
    """

    anim: animation.FuncAnimation = make_anim(frames)
    anim.save(filename + ".gif")
    return anim.to_jshtml()


def to_numpy(fig: plt.Figure) -> np.ndarray:
    """
    Convert Figure into numpy array

    Parameters
    ------
    fig: matplotlib.pyplot.Figure
        Figure which you want to convert into numpy array

    Reference
    ------
    https://pystyle.info/matplotlib-convert-figure-to-bytes-and-base64/
    """
    # Figure をレンダリングする。
    fig.canvas.draw()

    # 画像をバイト列で取得する。
    data: str = fig.canvas.tostring_rgb()

    # 画像の大きさを取得する。
    w, h = fig.canvas.get_width_height()
    channel_num: int = len(data) // (w * h)

    # numpy 配列に変換する
    img: np.ndarray = np.frombuffer(data, dtype=np.uint8).reshape(h, w, channel_num)
    return img
