import tools.getResourceAsStrings
import kotlin.test.Test

sealed interface Operation {
    fun apply(orig: String): String
    fun reverse(orig: String): String
}

data class SwapPosition(val x: Int, val y: Int) : Operation {
    override fun apply(orig: String) = orig.toCharArray().also {
        val tmp = it[x]
        it[x] = it[y]
        it[y] = tmp
    }.let { String(it) }

    override fun reverse(orig: String) = apply(orig)
}

data class SwapLetter(val x: Char, val y: Char) : Operation {
    override fun apply(orig: String) = orig.replace(x, '#').replace(y, x).replace('#', y)
    override fun reverse(orig: String) = apply(orig)
}

data class RotateLeft(val x: Int) : Operation {
    override fun apply(orig: String) = orig.substring(x % orig.length) + orig.substring(0, x % orig.length)
    override fun reverse(orig: String) = RotateRight(x).apply(orig)
}

data class RotateRight(val x: Int) : Operation {
    override fun apply(orig: String) = orig.substring(orig.length - x % orig.length) + orig.substring(0, orig.length - x % orig.length)
    override fun reverse(orig: String) = RotateLeft(x).apply(orig)
}

data class RotateBasedOnPositionOfLetter(val x: Char) : Operation {
    override fun apply(orig: String) = RotateRight(orig.indexOf(x) + (if (orig.indexOf(x) >= 4) 2 else 1)).apply(orig)
    override fun reverse(orig: String) = orig.indices.map { RotateLeft(it).apply(orig) }.first { apply(it) == orig }
}

data class ReversePositions(val x: Int, val y: Int) : Operation {
    override fun apply(orig: String) = orig.substring(0, x) + orig.substring(x, y + 1).reversed() + orig.substring(y + 1)
    override fun reverse(orig: String) = apply(orig)
}

data class MovePosition(val x: Int, val y: Int) : Operation {
    override fun apply(orig: String) = orig.removeRange(x, x + 1).let {
        it.substring(0, y) + orig[x] + it.substring(y)
    }
    override fun reverse(orig: String) = MovePosition(y, x).apply(orig)
}

class aoc21 {

    fun parseInput(file: String) = getResourceAsStrings(file).map {
        val s = it.trim().split(" ")
        when {
            s[0] == "swap" && s[1] == "position" -> SwapPosition(s[2].toInt(), s[5].toInt())
            s[0] == "swap" && s[1] == "letter" -> SwapLetter(s[2].single(), s[5].single())
            s[0] == "rotate" && s[1] == "left" -> RotateLeft(s[2].toInt())
            s[0] == "rotate" && s[1] == "right" -> RotateRight(s[2].toInt())
            s[0] == "rotate" && s[1] == "based" -> RotateBasedOnPositionOfLetter(s[6].single())
            s[0] == "reverse" -> ReversePositions(s[2].toInt(), s[4].toInt())
            s[0] == "move" -> MovePosition(s[2].toInt(), s[5].toInt())
            else -> throw Exception("Unknown operation")
        }
    }

    @Test
    fun part1() {
        val input = parseInput("/21/input.txt")
        var result = "abcdefgh"
        input.forEach { result = it.apply(result) }
        println(result)
    }

    @Test
    fun part2() {
        val input = parseInput("/21/input.txt").reversed()
        var result = "fbgdceah"
        input.forEach { result = it.reverse(result) }
        println(result)
    }
}