import numpy as np


def is_power_of_two(n):
    return (n != 0) and (n & (n - 1) == 0)


def get_angles(x):
    # convert to array
    x = np.array(x)
    shape = x.shape
    if len(shape) == 1:
        x = np.expand_dims(x, axis=0)

    if x.shape[1] == 1:
        x = x.T

    # get recursively the angles
    def angles(y, wire):
        d = y.shape[-1]
        if d == 2:
            thetas = np.arccos(y[:, 0] / np.linalg.norm(y, 2, 1))
            signs = (y[:, 1] > 0.).astype(int)
            thetas = signs * thetas + (1. - signs) * (2. * np.pi - thetas)
            thetas = np.expand_dims(thetas, 1)
            wires = [(wire, wire + 1)]
            return thetas, wires
        else:
            thetas = np.arccos(
                np.linalg.norm(y[:, :d // 2], 2, 1, True) /
                np.linalg.norm(y, 2, 1, True))
            thetas_l, wires_l = angles(y[:, :d // 2], wire)
            thetas_r, wires_r = angles(y[:, d // 2:], wire + d // 2)
            thetas = np.concatenate([thetas, thetas_l, thetas_r], axis=1)
            wires = [(wire, wire + d // 2)] + wires_l + wires_r
        return thetas, wires

    # result
    thetas, wires = angles(x, 0)

    # remove nan and one dims
    thetas = np.nan_to_num(thetas, nan=0)
    thetas = thetas.squeeze()

    return thetas, wires
