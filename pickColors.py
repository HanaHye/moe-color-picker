# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pyperclip


plt.ion()
plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']
plt.rcParams['font.size'] = 12
plt.rcParams['keymap.save'] = ''
plt.rcParams['keymap.pan'] = ''


def rgb2hex(rgb):
    return '#%6s' % hex((rgb[0] << 16) + (rgb[1] << 8) + rgb[2])[2:].zfill(6)


def onclick(event):
    global img
    global ax
    global rgb
    global colors

    x = int(round(event.xdata))
    y = int(round(event.ydata))
    rgb = img[y][x]
    print('rgb' + str(tuple(rgb)))
    colhex = rgb2hex(rgb)

    fig2 = plt.figure(figsize=(5, 5))
    fig2.canvas.mpl_connect('key_press_event', onpress_2)
    col1 = np.array([[rgb] * 60*vw] * 20*vw)
    col2 = np.array([[colors[-1]] * 60*vw] * 20*vw)
    col3 = np.array([[rgb] * 60*vw] * 20*vw)
    plt.imshow(np.vstack((col1, col2, col3)))
    plt.title('t-设为标题颜色 l-设为左栏颜色 b-设为底栏颜色')
    plt.text(30*vw, 10*vw, colhex, fontsize=40, ha='center', va='center', c='black')
    plt.text(30*vw, 30*vw, colhex, fontsize=40, ha='center', va='center', c=colhex)
    plt.text(30*vw, 50*vw, colhex, fontsize=40, ha='center', va='center', c='white')


def onpress_1(event):
    global colors

    if event.key == 'p':
        fig3 = plt.figure(figsize=(6, 10))
        tbar = np.array([[colors[0]] * dims[1]] * 20*vw)
        lbar = np.array([[colors[1]] * round(dims[1] / 3)] * 50*vw)
        rbar = np.array([[colors[3]] * round(dims[1] * 2 / 3)] * 50*vw)
        bbar = np.array([[colors[2]] * dims[1]] * 10*vw)
        col = np.vstack((tbar, img, np.hstack((lbar, rbar)), bbar))
        plt.title('效果预览', loc='center')
        plt.text(dims[1]/2, 10*vw, '标题文字', ha='center', va='center', c='white')
        plt.text(dims[1]/6, 45*vw + dims[0], '左栏', ha='center', va='center', c='black')
        plt.text(dims[1]*2/3, 45*vw + dims[0], '右栏', ha='center', va='center', c='black')
        plt.text(dims[1]/2, 75*vw + dims[0], '底栏文字', ha='center', va='center', c='white')
        plt.imshow(col)
        print(['rgb' + str(tuple(rgb)) for rgb in colors[:-1]])

    if event.key == 'c':
        plt.close()
        print('已保存到剪贴板，', [rgb2hex(rgb) for rgb in colors])
        pyperclip.copy(f'\n|标题颜色={rgb2hex(colors[0])}\n|左栏颜色={rgb2hex(colors[1])}\n|底栏颜色={rgb2hex(colors[2])}\n')


def onpress_2(event):
    global rgb
    global colors

    key = event.key
    if key == 't':
        colors[0] = rgb
        plt.close()
    elif key == 'l':
        colors[1] = rgb
        plt.close()
    elif key == 'b':
        colors[2] = rgb
        plt.close()


if __name__ == "__main__":
    path = input('输入图片文件路径：\n').strip('"').strip('file:///')
    colors = [[38, 202, 155, 255], [224, 255, 255, 255], [98, 188, 169, 255],
              [255, 255, 255, 255]]
    # Clipping input data to the valid range for imshow with RGB data
    # ValueError: invalid PNG header
    img = mpimg.imread(path, 0)
    dims = np.shape(img)
    vw = round(dims[1] / 100)
    if dims[2] == 3:
        colors = [color[:3] for color in colors]

    fig = plt.figure(figsize=(6, 6))
    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('key_press_event', onpress_1)
    plt.imshow(img)
    plt.title('鼠标点击取色，按p预览，按c保存到剪贴板', loc='center')
