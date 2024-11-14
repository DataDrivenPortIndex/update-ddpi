import argparse
import pandas as pd
import geopandas as gpd


parser = argparse.ArgumentParser()
parser.add_argument("ddpi")
parser.add_argument("ddpi_new")
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


def set_temporary_ddpi_id(gdf: gpd.GeoDataFrame, start_index: int) -> gpd.GeoDataFrame:
    print(start_index, len(gdf))
    gdf["ddpi_id"] = [start_index + i for i in range(len(gdf))]   
    
    return gdf


def main():
    df_l = gpd.read_file(args.ddpi)
    df_r = gpd.read_file(args.ddpi_new)

    df_r = set_temporary_ddpi_id(df_r, len(df_l))

    gdf = pd.concat([df_l, df_r]).reset_index(drop=True)

    while True:
        number_of_ports = len(gdf)

        gdf = spatial_join(gdf)

        if number_of_ports == len(gdf):
            break

    gdf = spatial_join(gdf)

    gdf.to_file("new_ddpi.geojson", driver="GeoJson")



if __name__ == "__main__":
    main()
