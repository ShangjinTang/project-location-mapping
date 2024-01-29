package com.example.locationinterestdetection;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.Point;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryCollection;

public class MapUtils {
    public static boolean isInsideAnyPolygon(Coordinate coordinate, GeometryCollection geometryCollection) {
        Point point = new GeometryFactory().createPoint(coordinate);
        for (int i = 0; i < geometryCollection.getNumGeometries(); i++) {
            Geometry geometry = geometryCollection.getGeometryN(i);
            if (geometry.contains(point)) {
                return true;
            }
        }
        return false;
    }
}