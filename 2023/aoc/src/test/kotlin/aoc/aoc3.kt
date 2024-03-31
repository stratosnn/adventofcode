package aoc

import org.example.tools.getResourceAsStrings
import org.junit.jupiter.api.Test

class aoc3 {

    private fun neighbours(x: Int, y: Int, rangeX: IntRange, rangeY: IntRange) =
        (x - 1 .. x + 1).flatMap { rx -> (y - 1 .. y + 1).map { ry -> rx to ry } }
            .filter { p -> p != (x to y) && (p.first in rangeX) && (p.second in rangeY) }

    private fun isPart(neighbourCells: Set<Pair<Int, Int>>, data: List<String>) =
        neighbourCells.map { (x, y) -> data[y][x] }
            .any { !it.isDigit() && it != '.' }

    @Test
    fun part1() {
        val data = getResourceAsStrings("/3/input1.txt")
        val parts = data.flatMapIndexed { lineIx, s ->
            val seq = sequence {
                val neighbourCells = mutableSetOf<Pair<Int, Int>>()
                val numberAsString = StringBuilder()
                for ((ix, c) in s.withIndex()) {
                    if (c.isDigit()) {
                        neighbourCells.addAll(neighbours(ix, lineIx, s.indices, data.indices))
                        numberAsString.append(c)
                    } else if (neighbourCells.isNotEmpty()) {
                        if (isPart(neighbourCells, data)) {
                            yield(numberAsString.toString().toInt())
                        }
                        numberAsString.clear()
                        neighbourCells.clear()
                    }
                }
                if (isPart(neighbourCells, data)) {
                    yield(numberAsString.toString().toInt())
                }
            }
            seq.toList()
        }
        println(parts.sum())
    }

    @Test
    fun part2() {
        val data = getResourceAsStrings("/3/input1.txt")
        val partsMap = data.flatMapIndexed { lineIx, s ->
            val seq = sequence {
                val neighbourCells = mutableSetOf<Pair<Int, Int>>()
                val numberAsString = StringBuilder()
                for ((ix, c) in s.withIndex()) {
                    if (c.isDigit()) {
                        neighbourCells.addAll(neighbours(ix, lineIx, s.indices, data.indices))
                        numberAsString.append(c)
                    } else if (neighbourCells.isNotEmpty()) {
                        neighbourCells.filter { (x, y)  ->
                            val chr = data[y][x]
                            !chr.isDigit() && chr != '.'
                        }.forEach { point -> yield(point to numberAsString.toString().toInt()) }
                        numberAsString.clear()
                        neighbourCells.clear()
                    }
                }
                neighbourCells.filter { (x, y)  ->
                    val chr = data[y][x]
                    !chr.isDigit() && chr != '.'
                }.forEach { point -> yield(point to numberAsString.toString().toInt()) }
            }
            seq.toList()
        }

        val result = partsMap.groupBy( { it.first }, { it.second })
            .filter { (point, values) -> data[point.second][point.first] == '*' && values.size == 2 }
            .values
            .sumOf { it[0] * it[1] }

        println(result)

    }
}