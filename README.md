# simple-local-relief-visualizer

Python tool for generating Simple Local Relief Model (SLRM) visualizations from LiDAR DEMs, aimed at archaeological prospection.

SLRM subtracts a Gaussian-smoothed version of the terrain from the original DEM. This removes large-scale topography and highlights small features such as barrows, ditches and banks. All GeoTIFFs in a folder are processed in one run.

## Requirements

- Python 3.9+
- rasterio, NumPy, SciPy

```bash
pip install rasterio numpy scipy
```

## Usage

```bash
git clone https://github.com/leonsmolej/simple-local-relief-visualizer.git
cd simple-local-relief-visualizer
python main.py
```

The program asks for:

| Input | Description | Suggested |
|---|---|---|
| DEM folder | Path to the folder with `.tif` / `.tiff` files | - |
| Gaussian filter radius | In pixels (0 to 500) | 20 for small features, 40 for larger ones |
| Minimum value | Lower clipping value (-10 to 0) | -1.5 |
| Maximum value | Upper clipping value (0 to 10) | 1.5 |

To convert a radius from meters to pixels, divide it by the DEM resolution (e.g. 20 m on a 0.5 m DEM = 40 pixels).

## Output

Results are saved to `Rezultati_SLRM/SLRM_<name>.tif` inside the input folder. Existing files with the same name are overwritten.

## Notes

- Use DEMs in a projected coordinate system (e.g. EPSG:3794) so pixels correspond to meters.
- Only the first band is processed, and NoData values are not masked.

## License

MIT. See [LICENSE](LICENSE).
