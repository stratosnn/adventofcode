package org.example.tools

import kotlin.math.abs


data class Point2D(
    val x: Int,
    val y: Int,
) {
    constructor(pair: Pair<Int, Int>) : this(pair.first, pair.second)

    fun neighbors(
        rangeX: IntRange? = null,
        rangeY: IntRange? = null,
        includeDiagonals: Boolean = false,
    ) = buildList {
        addAll(listOf(
            Point2D(x - 1, y),
            Point2D(x + 1, y),
            Point2D(x, y - 1),
            Point2D(x, y + 1),
        ))
        if (includeDiagonals) {
            addAll(listOf(
                Point2D(x - 1, y - 1),
                Point2D(x - 1, y + 1),
                Point2D(x + 1, y - 1),
                Point2D(x + 1, y + 1),
            ))
        }
    }.filter { p ->
        (rangeX?.let { p.x in it } ?: true) && (rangeY?.let { p.y in it } ?: true)
    }

    operator fun plus(other: Point2D) = Point2D(x + other.x, y + other.y)
    operator fun minus(other: Point2D) = Point2D(x - other.x, y - other.y)
    operator fun times(factor: Int) = Point2D(x * factor, y * factor)
    operator fun times(other: Point2D) = Point2D(x * other.x, y * other.y)

    fun determinant(other: Point2D) =  x.toLong() * other.y.toLong() - y.toLong() * other.x.toLong()

    fun rotate(degrees: Int) = when (degrees) {
        0 -> this
        90 -> Point2D(y, -x)
        180 -> Point2D(-x, -y)
        270 -> Point2D(-y, x)
        else -> throw IllegalArgumentException("Invalid degrees: $degrees")
    }

    fun manhattanDistance(other: Point2D) = abs(x - other.x) + abs(y - other.y)

    companion object {
        val S = Point2D(0  to +1) // inverted to be aligned with the grid
        val N = Point2D(0  to -1)
        val E = Point2D(+1 to 0)
        val W = Point2D(-1 to 0)

        fun fromDirectionString(direction: String) = when (direction) {
            "S", "D" -> S
            "N", "U" -> N
            "E", "R" -> E
            "W", "L" -> W
            else -> throw IllegalArgumentException("Invalid direction: $direction")
        }
    }
}