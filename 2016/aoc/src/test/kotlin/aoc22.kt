import com.github.shiguruikai.combinatoricskt.permutations
import tools.Point2D
import tools.getResourceAsStrings
import kotlin.test.Test

class aoc22 {

    companion object {
        val pattern = Regex("/dev/grid/node-x(\\d+)-y(\\d+)\\s+(\\d+)T\\s+(\\d+)T\\s+(\\d+)T\\s+(\\d+)%")
    }

    data class Node(
        val position: Point2D,
        val size: Int,
        val used: Int,
        val avail: Int,
        val usePerc: Int
    ) {
        val name
            get() = "/dev/grid/node-x${position.x}-y${position.y}"
    }

    fun parseInput(file: String) = getResourceAsStrings(file).drop(2).map {
        val match = pattern.find(it)
        val (x, y, size, used, avail, usePerc) = match!!.destructured
        Node(Point2D(x.toInt(), y.toInt()), size.toInt(), used.toInt(), avail.toInt(), usePerc.toInt())
    }

    @Test
    fun part1() {
        val nodes = parseInput("/22/input.txt")
        val viablePairs = nodes.permutations(2).filter { (a, b) -> a.used > 0 && a.used <= b.avail }.toList()
        println(viablePairs.size)
    }

    @Test
    fun part2() {
        val nodes = parseInput("/22/input.txt")
        val nodesMap = nodes.associateBy { it.position }
        val maxX = nodes.maxOf { it.position.x }.toInt()
        val maxY = nodes.maxOf { it.position.y }.toInt()
        val vault = nodesMap[Point2D(maxX, 0)]!!
        val empty = nodes.first { it.used == 0 }

        println("vault: $vault")
        println("empty: $empty")

        println(nodes.filter {it.avail >= vault.used})

        nodes.forEach {
            val neighbours = it.position.neighbors(0..maxX, 0..maxY)
            val moveable = neighbours.filter { n -> nodesMap[n]!!.avail >= it.used }
            if (moveable.isNotEmpty()) {
                println("${it.name} can move to ${moveable.joinToString { nodesMap[it]!!.name }}")
            }
        }

        nodes.filter { it.used > empty.size }.forEach { println(it) }

        // empty (x=24, y=22)
        // going up to the wall: 22 - 12 - 1 = 9 (x=24, y=13)
        // going left along the wall: 24 - 9 + 1 = 16 (x=8, y=13)
        // going up to the top: 13  (x=8, y=0)
        // going right next to the vault: 30 - 8 = 22 (x=30, y=0)
        // move around vault content to the left: 5 moves for each square: 5 * ( 31 - 0 - 1 ) + 1 (last) = 151

        println(9 + 16 + 13 + 22 + 151)

    }

}