import os
import argparse
import pandas as pd
import geopandas as gpd


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--existing", type=str, help="enter the existing ddpi file")
parser.add_argument("-n", "--new", type=str, help="enter the new ddpi file")
parser.add_argument("-o", "--output", type=str, help="enter the output file")
args = parser.parse_args()


def spatial_join(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf = gdf.sjoin(gdf, how="left", predicate="intersects")
    gdf = gdf.dissolve("ddpi_id_right")

    gdf = gdf.reset_index().dissolve("ddpi_id_left")

    gdf = gdf.drop(
        ["ddpi_id_right", "is_anchorage_right", "index_right"], axis=1
    ).reset_index()

    return gdf.rename(
        columns={"ddpi_id_left": "ddpi_id", "is_anchorage_left": "is_anchorage"}
    )


def set_ddpi_id(gdf: gpd.GeoDataFrame, start_index: int) -> gpd.GeoDataFrame:
    gdf["ddpi_id"] = [start_index + i for i in range(len(gdf))]

    return gdf


def write_geojson(gdf: gpd.GeoDataFrame, file_name: str):
    if os.path.isfile(file_name):
        os.remove(file_name)

    gdf.to_file(file_name, driver="GeoJson")


def main():
    df_l = gpd.read_file(args.existing)
    df_r = gpd.read_file(args.new)

    df_r = set_ddpi_id(df_r, len(df_l))

    gdf = pd.concat([df_l, df_r]).reset_index(drop=True)

    # remove combine overlapping polygons
    while True:
        number_of_ports = len(gdf)

        # perform spation join to combine overlapping polygons
        gdf = spatial_join(gdf)

        # check if no further overlaps where found
        if number_of_ports == len(gdf):
            break

    write_geojson(gdf, args.output)


if __name__ == "__main__":
    main()
