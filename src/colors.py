"""
All logic for sampling the main colors of the track cover
"""
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import colour as cl
import matplotlib.pyplot as plt


def rgb_to_lab(rgb_array: np.array) -> np.array:
    RGB_to_XYZ_matrix = np.array(
        [
            [0.41240000, 0.35760000, 0.18050000],
            [0.21260000, 0.71520000, 0.07220000],
            [0.01930000, 0.11920000, 0.95050000]
        ]
    )
    i_RGB = np.array([0.31270, 0.32900])
    i_XYZ = np.array([0.34570, 0.35850])
    xyz_array = cl.RGB_to_XYZ(
        rgb_array / 255.0, i_RGB, i_XYZ, RGB_to_XYZ_matrix, "Bradford"
    )

    return cl.XYZ_to_Lab(xyz_array)


def lab_to_rgb(lab_array: np.array) -> np.array:
    xyz_array = cl.Lab_to_XYZ(lab_array)
    XYZ_to_RGB_matrix = np.array(
        [
            [3.24062548, -1.53720797, -0.49862860],
            [-0.96893071, 1.87575606, 0.04151752],
            [0.05571012, -0.20402105, 1.05699594]
        ]
    )
    i_RGB = np.array([0.31270, 0.32900])
    i_XYZ = np.array([0.34570, 0.35850])
    rgb_array = cl.XYZ_to_RGB(
        xyz_array, i_XYZ, i_RGB, XYZ_to_RGB_matrix, "Bradford"
    ) * 255

    return rgb_array


def sortColors(colors: list) -> list:
    return sorted(colors, key=lambda c: cl.RGB_to_HCL(c)[2])


def imageToArray(file: str, resizeTo: tuple = (80, 80)) -> list:
    cover_image = Image.open(file).resize(resizeTo)
    pixels = np.array(cover_image.getdata())

    return pixels


def getColors(file: str, n_colors: int) -> list:
    pixels = imageToArray(file)

    kmeans = KMeans(n_clusters=n_colors, n_init="auto", max_iter=1000)
    kmeans = kmeans.fit(rgb_to_lab(pixels))
    clusters = kmeans.cluster_centers_
    clusters = lab_to_rgb(clusters)

    return clusters


def plotColors(file: str, displayClusters: bool):
    rgb_array = list(imageToArray(file, resizeTo=(160, 160)))
    colors = getColors(file, 3)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    x, y, z, s = [], [], [], []
    for value in rgb_array:
        x.append(value[0])
        y.append(value[1])
        z.append(value[2])
        s.append(7)

    if displayClusters:
        for value in colors:
            x.append(value[0])
            y.append(value[1])
            z.append(value[2])
            rgb_array.append((0, 255, 0))
            s.append(100)

    ax.scatter(x, y, z, c=np.array(rgb_array) / 255.0, s=s)

    ax.set_xlabel("Rojo")
    ax.set_ylabel("Verde")
    ax.set_zlabel("Azul")

    plt.show()


if __name__ == "__main__":
    import requests
    from io import BytesIO
    from spotify import getTrackID, getTrackInfo

    n_colors = 6
    # Thanks fuzzy search :)
    track = "starboy"

    id = getTrackID(track)
    info = getTrackInfo(id)

    url = info["album"]["images"][0]["url"]

    response = requests.get(url)
    track_image_file = BytesIO(response.content)

    plotColors(track_image_file, False)

    colors = getColors(track_image_file, n_colors)

    plt.imshow([sortColors(colors / 255.0)])
    plt.show()
