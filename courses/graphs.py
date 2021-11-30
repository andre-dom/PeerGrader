from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np


def generateGradeChart(data, maxScore):
    data = np.random.normal(0, 10, 50)
    plt.clf()
    bins = np.arange(maxScore + 2) - 0.5
    plt.hist(data, facecolor='#4582ec', edgecolor="#343a40", bins=bins)
    plt.ylabel('Num Students')
    plt.xlabel('Score')
    plt.tight_layout()
    # plt.style.use('seaborn-pastel')
    print(plt.style.available)
    plt.locator_params(axis="both", integer=True, tight=True)
    # plt.xticks(np.arange(0, max(data) + 1, 1.0))



    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic


# def generateGradeChart(data, maxScore):
#     hist = pygal.Histogram()
#     for
#     hist.add('Scores', [(5, 0, 10), (4, 5, 13), (2, 0, 15)])
#
#     return graphic