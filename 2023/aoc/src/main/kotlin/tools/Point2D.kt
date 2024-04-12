package org.example.tools


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
}