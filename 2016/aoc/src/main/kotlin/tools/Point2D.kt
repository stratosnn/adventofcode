package tools

import kotlin.math.abs


data class Point2D(
    val x: Long,
    val y: Long,
) {
    constructor(pair: Pair<Long, Long>) : this(pair.first, pair.second)
    constructor(x: Int, y: Int) : this(x.toLong(), y.toLong())

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
    operator fun times(factor: Long) = Point2D(x * factor, y * factor)
    operator fun times(other: Point2D) = Point2D(x * other.x, y * other.y)

    fun determinant(other: Point2D) =  x * other.y - y * other.x
    fun determinantDouble(other: Point2D) =  x.toDouble() * other.y.toDouble() - y.toDouble() * other.x.toDouble()


    fun rotate(degrees: Int) = when (degrees) {
        0 -> this
        90 -> Point2D(y, -x)
        180 -> Point2D(-x, -y)
        270 -> Point2D(-y, x)
        else -> throw IllegalArgumentException("Invalid degrees: $degrees")
    }

    fun manhattanDistance(other: Point2D) = abs(x - other.x) + abs(y - other.y)

    companion object {
        val S = Point2D(0L  to +1L) // inverted to be aligned with the grid
        val N = Point2D(0L  to -1L)
        val E = Point2D(+1L to 0L)
        val W = Point2D(-1L to 0L)

        fun fromDirectionString(direction: String) = when (direction) {
            "S", "D" -> S
            "N", "U" -> N
            "E", "R" -> E
            "W", "L" -> W
            else -> throw IllegalArgumentException("Invalid direction: $direction")
        }
    }
}
