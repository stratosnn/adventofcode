package aoc

import org.example.tools.Point2D
import org.example.tools.getResourceAsStrings
import java.util.*
import kotlin.test.Test

class aoc22 {

    data class Brick(val id: Int, val cubes: List<Pair<Point2D, Int>>) {
        val minZ
            get() = cubes.minOf { it.second }
        val below = mutableSetOf<Brick>()
        val above = mutableSetOf<Brick>()
    }

    fun parseInput(file: String) = getResourceAsStrings(file).mapIndexed { ix, line ->
        val p = line.trim().split(',', '~').map { it.toInt() }
        val (xr, yr, zr) = arrayOf(p[0]..p[3], p[1]..p[4], p[2]..p[5])
        val cubes = xr.flatMap { x -> yr.flatMap { y -> zr.map { z -> Point2D(x, y) to z } } }
        Brick(ix, cubes)
    }

    fun List<Brick>.settle() = this
        .sortedBy { brick -> brick.cubes.minOf { it.second } }
        .let { input ->
            val settled = mutableListOf<Brick>()
            val grid = mutableMapOf<Point2D, TreeMap<Int, Brick>>()

            input.forEach { brick ->
                val maybeBelow = brick.cubes
                    .mapNotNull { (point, z) -> grid.getOrPut(point) { TreeMap() }.lowerEntry(z) }
                    .map { (k, v)  -> k to v }
                val settledBrick = if (maybeBelow.isEmpty()) {
                    val offset = brick.minZ - 1
                    brick.copy(cubes = brick.cubes.map { (point, z) -> point to z - offset })
                } else {
                    val maxZ = maybeBelow.maxOf { it.first }
                    val offset = brick.minZ - maxZ - 1
                    brick.copy(cubes = brick.cubes.map { (point, z) -> point to z - offset }).also { newBrick ->
                        maybeBelow.filter { it.first == maxZ }
                            .forEach { (_, belowBrick) ->
                                newBrick.below.add(belowBrick)
                                belowBrick.above.add(newBrick)
                            }
                    }
                }

                settled.add(settledBrick)
                settledBrick.cubes.forEach { (point, z) ->
                    grid.getOrPut(point) { TreeMap() }[z] = settledBrick
                }
            }
            settled
        }

    fun Brick.chainReaction(willFall: MutableSet<Brick>): MutableSet<Brick> =
        willFall.also {
            if (below.isNotEmpty() && below.all { it in willFall }) {
                willFall.add(this)
            }
            above.forEach { it.chainReaction(willFall) }
        }


    @Test
    fun part1() {
        val settled = parseInput("/22/input.txt").settle()
        val structural = settled.filter { brick -> brick.above.any { it.below.size == 1 } }
        println(settled.count() - structural.count())
    }

    @Test
    fun part2() {
        val settled = parseInput("/22/input.txt").settle()
        val structural = settled.filter { brick -> brick.above.any { it.below.size == 1 } }
        val res = structural.map { it.chainReaction(mutableSetOf(it)) }
            .sumOf { it.size - 1 }

        println(res)
    }
}