package aoc

import com.github.shiguruikai.combinatoricskt.combinations
import org.example.tools.Point2D
import org.example.tools.Point3D
import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc24 {

    fun parseInput(file: String) = getResourceAsStrings(file).map { line ->
        val (left, right) = line.split(" @ ")
        val p = left.split(',').map { it.trim().toBigInteger() }
        val v = right.split(',').map { it.trim().toBigInteger() }
        Point3D(p[0], p[1], p[2]) to Point3D(v[0], v[1], v[2])
    }

    @Test
    fun part1() {
        val input = parseInput("/24/input.txt").map { (p, v) -> Point2D(p.x.toLong(), p.y.toLong()) to Point2D(v.x.toLong(), v.y.toLong()) }

        val allowedRange = 200000000000000.0..400000000000000.0

        val possibleCollisions = input.combinations(2).mapNotNull { (s1, s2) ->
            // Using cramer's rule to solve 2D system of equations
            val (p1, v1) = s1
            val (p2, v2) = s2
            val a = Point2D(-v1.y, -v2.y)
            val b = Point2D(v1.x, v2.x)
            val c1 = Point2D(v1.x, v1.y).determinant(Point2D(p1.x, p1.y))
            val c2 = Point2D(v2.x, v2.y).determinant(Point2D(p2.x, p2.y))
            val c = Point2D(c1, c2)
            val det = a.determinant(b)

            det.takeIf { it != 0L }
                ?.let { c.determinantDouble(b)/it to a.determinantDouble(c)/it }
                ?.takeIf { intersection ->
                    listOf(
                        (intersection.first - p1.x) / v1.x,
                        (intersection.second - p1.y) / v1.y,
                        (intersection.first - p2.x) / v2.x,
                        (intersection.second - p2.y) / v2.y
                    ).all { it >= 0 }
                }
        }.filter { (x, y) -> x in allowedRange && y in allowedRange }

        println(possibleCollisions.count())
    }

    @Test
    fun part2() {
        val d = parseInput("/24/input.txt")
        val (p0, v0) = d[0]
        val (position1, velocity1) = d[1]
        val (position2, velocity2) = d[2]
        val (p1, v1) = position1 - p0 to velocity1 - v0
        val (p2, v2) = position2 - p0 to velocity2 - v0

        val t1 = -(p1.crossProduct(p2).dotProduct(v2)) / v1.crossProduct(p2).dotProduct(v2)
        val t2 = -(p1.crossProduct(p2).dotProduct(v1)) / p1.crossProduct(v2).dotProduct(v1)

        val c1 = position1 + (velocity1 * t1)
        val c2 = position2 + (velocity2 * t2)

        val v = (c2 - c1) / (t2 - t1)
        val p = c1 - v * t1
        println(p.x + p.y + p.z)
    }
}