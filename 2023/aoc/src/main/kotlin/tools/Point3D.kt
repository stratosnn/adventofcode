package org.example.tools

import java.math.BigInteger

data class Point3D(
    val x: BigInteger,
    val y: BigInteger,
    val z: BigInteger
) {
    constructor(pair: Triple<BigInteger, BigInteger, BigInteger>) : this(pair.first, pair.second, pair.third)

    operator fun plus(other: Point3D) = Point3D(x + other.x, y + other.y, z + other.z)
    operator fun minus(other: Point3D) = Point3D(x - other.x, y - other.y, z - other.z)
    operator fun times(factor: BigInteger) = Point3D(x * factor, y * factor, z * factor)
    operator fun times(other: Point3D) = Point3D(x * other.x, y * other.y, z * other.z)
    operator fun div(factor: BigInteger) = Point3D(x / factor, y / factor, z / factor)
    operator fun div(other: Point3D) = Point3D(x / other.x, y / other.y, z / other.z)

    fun dotProduct(other: Point3D) = x * other.x + y * other.y + z * other.z

    fun crossProduct(other: Point3D) = Point3D(
        (y * other.z - z * other.y),
        (z * other.x - x * other.z),
        (x * other.y - y * other.x),
    )

}
