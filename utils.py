
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon

def plot_tubule_patch(gdf, img, tubule_id="929", buffer=200):

    tubule = gdf[gdf["id"] == str(tubule_id)]

    if tubule.empty:
        raise ValueError(f"Tubule {tubule_id} not found")

    geom = tubule.geometry.iloc[0]

    minx, miny, maxx, maxy = geom.bounds

    minx -= buffer
    miny -= buffer
    maxx += buffer
    maxy += buffer

    width, height = img.size

    minx = max(0, int(minx))
    miny = max(0, int(miny))
    maxx = min(width, int(maxx))
    maxy = min(height, int(maxy))

    crop = img.crop((minx, miny, maxx, maxy))

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(crop)

    def plot_geom(g):

        if isinstance(g, Polygon):

            x, y = g.exterior.xy

            x = [xi - minx for xi in x]
            y = [yi - miny for yi in y]

            ax.plot(x, y, color="red", linewidth=2)

        elif isinstance(g, MultiPolygon):

            for poly in g.geoms:
                plot_geom(poly)

    plot_geom(geom)

    ax.set_ylim(crop.size[1], 0)

    ax.set_title(f"Tubule {tubule_id}")

    plt.show()

    return crop
