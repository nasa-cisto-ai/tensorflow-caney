import xarray as xr
from typing import List

__all__ = [
    "bai", "cig", "cire", "cm", "cs1", "cs2",
    "dvi", "dwi", "fdi", "gndvi", "ndvi", "ndwi",
    "si", "sr", "_get_band_locations", "_get_index_function",
    "add_indices"
]


# ---------------------------------------------------------------------------
# Get Methods
# ---------------------------------------------------------------------------
def _get_band_locations(bands: list, requested_bands: list) -> List:
    """
    Get list indices for band locations.
    Args:
        bands (list): list of bands in the original raster
        requested_bands (list): list of requested bands for indices
    Returns:
        List of band locations in the order received.
    """
    locations = []
    for b in requested_bands:
        try:
            locations.append(bands.index(b.lower()))
        except ValueError:
            raise ValueError(f'{b} not in raster bands {bands}')
    return locations


# ---------------------------------------------------------------------------
# Indices Methods
# ---------------------------------------------------------------------------
def bai(raster):
    """
    Burn Area Index (BAI), BAI := 1/((0.1 -RED)^2 + (0.06 - NIR)^2)
    Args:
        raster (list): xarray or numpy array object in the form (c, h, w)
    Returns:
        new xarray.DataArray band with SI calculated
    """
    red, nir1 = _get_band_locations(
        raster.attrs['band_names'], ['red', 'nir1'])
    index = (
        1 / (
            (0.1 - raster[red, :, :]) ** 2 +
            (0.06 - raster[nir1, :, :]) ** 2)
    )
    return index.expand_dims(dim="band", axis=0)


def cig(raster):
    """
    Chlorophyll Index - Green (CIg), CIRE := (NIR / Green) - 1
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with SI calculated
    """
    nir1, green = _get_band_locations(
        raster.attrs['band_names'], ['nir1', 'green'])
    index = (raster[nir1, :, :] / raster[green, :, :]) - 1
    return index.expand_dims(dim="band", axis=0)


def cire(raster):
    """
    Chlorophyll Index - Red-Edge (CIre), CIRE := (NIR / RedEdge) - 1
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with SI calculated
    """
    bands = ['nir1', 'rededge']
    if not all(b in bands for b in raster.attrs['band_names']):
        bands = ['nir1', 'red']
    nir1, rededge = _get_band_locations(
        raster.attrs['band_names'], bands)
    index = (raster[nir1, :, :] / raster[rededge, :, :]) - 1
    return index.expand_dims(dim="band", axis=0)


def cm(raster):
    """
    Clay Minerals (CM), CM := SWIR1 / SWIR2
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with SI calculated
    """
    swir1, swir2 = _get_band_locations(
        raster.attrs['band_names'], ['swir1', 'swir2'])
    index = raster[swir1, :, :] / raster[swir2, :, :]
    return index.expand_dims(dim="band", axis=0)


def cs1(raster):
    """
    Cloud detection index (CS1), CS1 := (3. * NIR1) / (Blue + Green + Red)
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with SI calculated
    """
    nir1, red, blue, green = _get_band_locations(
        raster.attrs['band_names'], ['nir1', 'red', 'blue', 'green'])
    index = (
        (3. * raster[nir1, :, :]) /
        (raster[blue, :, :] + raster[green, :, :] + raster[red, :, :])
    )
    return index.expand_dims(dim="band", axis=0)


def cs2(raster):
    """
    Cloud detection index (CS2), CS2 := (Blue + Green + Red + NIR1) / 4.
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with CS2 calculated
    """
    nir1, red, blue, green = _get_band_locations(
        raster.attrs['band_names'], ['nir1', 'red', 'blue', 'green'])
    index = (
        (raster[blue, :, :] + raster[green, :, :]
            + raster[red, :, :] + raster[nir1, :, :])
        / 4.0
    )
    return index.expand_dims(dim="band", axis=0)


def dvi(raster):
    """
    Difference Vegetation Index (DVI), DVI := NIR1 - Red
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with DVI calculated
    """
    nir1, red = _get_band_locations(
        raster.attrs['band_names'], ['nir1', 'red'])
    index = (
        raster[nir1, :, :] - raster[red, :, :]
    )
    return index.expand_dims(dim="band", axis=0)


def dwi(raster):
    """
    Difference Water Index (DWI), DWI := Green - NIR1
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with DWI calculated
    """
    nir1, green = _get_band_locations(
        raster.attrs['band_names'], ['nir1', 'green'])
    index = (
        raster[green, :, :] - raster[nir1, :, :]
    )
    return index.expand_dims(dim="band", axis=0)


def evi(raster):
    """
    Shadow Index (SI), SI := (Blue * Green * Red) ** (1.0 / 3)
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with SI calculated
    """
    red, blue, nir1 = _get_band_locations(
        raster.attrs['band_names'], ['red', 'blue', 'nir1'])
    index = (
        (2.5 * (raster[nir1, :, :] - raster[red, :, :])) /
        (
            raster[nir1, :, :] + 6 * raster[red, :, :]
            - 7.5 * raster[blue, :, :] + 1)
    )
    return index.expand_dims(dim="band", axis=0)


def fdi(raster):
    """
    Forest Discrimination Index (FDI), type int16
    8 band imagery: FDI := NIR2 - (RedEdge + Blue)
    4 band imagery: FDI := NIR1 - (Red + Blue)
    :param data: xarray or numpy array object in the form (c, h, w)
    :return: new band with FDI calculated
    """
    bands = ['blue', 'nir2', 'rededge']
    if not all(b in bands for b in raster.attrs['band_names']):
        bands = ['blue', 'nir1', 'red']
    blue, nir, red = _get_band_locations(
        raster.attrs['band_names'], bands)
    index = (
        raster[nir, :, :] - (raster[red, :, :] + raster[blue, :, :])
    )
    return index.expand_dims(dim="band", axis=0)


def gndvi(raster):
    """
    Difference Vegetation Index (DVI), GNDVI := (NIR - Green) / (NIR + Green)
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with DVI calculated
    """
    nir1, green = _get_band_locations(
        raster.attrs['band_names'], ['nir1', 'green'])
    index = (
        (raster[nir1, :, :] - raster[green, :, :]) /
        (raster[nir1, :, :] + raster[green, :, :])
    )
    return index.expand_dims(dim="band", axis=0)


def ndvi(raster):
    """
    Difference Vegetation Index (DVI), NDVI := (NIR - Red) / (NIR + RED)
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with DVI calculated
    """
    nir1, red = _get_band_locations(
        raster.attrs['band_names'], ['nir1', 'red'])
    index = (
        (raster[nir1, :, :] - raster[red, :, :]) /
        (raster[nir1, :, :] + raster[red, :, :])
    )
    return index.expand_dims(dim="band", axis=0)


def ndwi(raster):
    """
    Normalized Difference Water Index (NDWI)
    NDWI := factor * (Green - NIR1) / (Green + NIR1)
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with SI calculated
    """
    nir1, green = _get_band_locations(
        raster.attrs['band_names'], ['nir1', 'green'])
    index = (
        (raster[green, :, :] - raster[nir1, :, :]) /
        (raster[green, :, :] + raster[nir1, :, :])
    )
    return index.expand_dims(dim="band", axis=0)


def si(raster):
    """
    Shadow Index (SI), SI := (Blue * Green * Red) ** (1.0 / 3)
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with SI calculated
    """
    red, blue, green = _get_band_locations(
        raster.attrs['band_names'], ['red', 'blue', 'green'])
    index = (
        (raster[blue, :, :] - raster[green, :, :] /
            raster[red, :, :]) ** (1.0/3.0)
    )
    return index.expand_dims(dim="band", axis=0)


def sr(raster):
    """
    SR := NIR / Red
    :param raster: xarray or numpy array object in the form (c, h, w)
    :return: new band with SI calculated
    """
    nir1, red = _get_band_locations(
        raster.attrs['band_names'], ['nir1', 'red'])
    index = (
        raster[nir1, :, :] / raster[red, :, :]
    )
    return index.expand_dims(dim="band", axis=0)


# ---------------------------------------------------------------------------
# Modify Methods
# ---------------------------------------------------------------------------
indices_registry = {
    'bai': bai,
    'cig': cig,
    'cire': cire,
    'cm': cm,
    'cs1': cs1,
    'cs2': cs2,
    'dvi': dvi,
    'dwi': dwi,
    'fdi': fdi,
    'gndvi': gndvi,
    'ndvi': ndvi,
    'ndwi': ndwi,
    'si': si,
    'sr': sr
}


def _get_index_function(index_key):
    """
    Get index function from the indices registry.
    """
    try:
        return indices_registry[index_key.lower()]
    except KeyError:
        raise ValueError(f'Invalid indices mapping: {index_key}.')


def add_indices(xraster, input_bands, output_bands, factor=1.0):
    """
    :param rastarr: xarray or numpy array object in the form (c, h, w)
    :param bands: list with strings of bands in the raster
    :param indices: indices to calculate and append to the raster
    :param factor: factor used for toa imagery
    :return: raster with updated bands list
    """

    # make band names uniform for easy of validation
    input_bands = [s.lower() for s in input_bands]
    output_bands = [s.lower() for s in output_bands]

    xraster.attrs['band_names'] = input_bands
    n_bands = len(input_bands)  # get number of input bands

    # iterate over each new band that needs to be included
    for band_id in output_bands:

        if band_id not in input_bands:

            # increase the number of input bands
            n_bands += 1

            # calculate band (indices)
            index_function = _get_index_function(band_id)
            new_index = index_function(xraster)

            # Add band indices to raster, add future object
            new_index.coords['band'] = [n_bands]
            xraster = xr.concat([xraster, new_index], dim='band')

            # Update raster metadata,
            xraster.attrs['band_names'].append(band_id)

    return xraster
