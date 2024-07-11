import tools.getResourceAsStrings
import kotlin.test.Test


class aoc15 {

    data class Disc(
        val id: Int,
        val period: Int,
        val position: Int,
    )

    val regex = """Disc #(?<id>\d+) has (?<period>\d+).*position (?<pos>\d+)\.""".toRegex()

    fun parseInput(fileName: String) = getResourceAsStrings(fileName).map {
        val match = regex.find(it)!!
        Disc(match.groups["id"]!!.value.toInt(), match.groups["period"]!!.value.toInt(), match.groups["pos"]!!.value.toInt())
    }

    @Test
    fun part1() {
        // here we can use chinese remainder theorem to solve it, but we just brute force it :D
        val constrains = parseInput("/15/input.txt").map { disc ->
            val rem = (disc.id + disc.position) % disc.period
            disc.period to (disc.period - rem) % disc.period
        }

        val result = generateSequence(0) { it + 1 }.first { x ->
            constrains.all { x % it.first == it.second }
        }

        println(result)
    }

    @Test
    fun part2() {
        val originalDiscs = parseInput("/15/input.txt").sortedBy { it.id }
        val constrains = buildList {
            addAll(originalDiscs)
            add(Disc(originalDiscs.last().id+1, 11, 0))
        }.map { disc ->
            val rem = (disc.id + disc.position) % disc.period
            disc.period to (disc.period - rem) % disc.period
        }

        val result = generateSequence(0) { it + 1 }.first { x ->
            constrains.all { x % it.first == it.second }
        }

        println(result)
    }
}