import org.junit.jupiter.api.Test

class aoc18 {

    companion object {
         const val INPUT = "^.^^^..^^...^.^..^^^^^.....^...^^^..^^^^.^^.^^^^^^^^.^^.^^^^...^^...^^^^.^.^..^^..^..^.^^.^.^......."
    }

    private fun nextTile(triple: String) = when (triple) {
        "^^." -> '^'
        ".^^" -> '^'
        "^.." -> '^'
        "..^" -> '^'
        else -> '.'
    }

    private fun nextRow(row: String): String {
        val padded = ".${row}."
        return (1..<padded.length-1).map { i -> padded.slice(i - 1..i + 1) }.map { nextTile(it) }.joinToString("")
    }

    private fun expand(row: String, times: Int): List<String> {
        return (1..times).scan(row) { acc, _ -> nextRow(acc) }
    }

    @Test
    fun part1() {
        println(expand(INPUT, 39).sumOf { row -> row.count { it == '.' } })
    }

    @Test
    fun part2() {
        println(expand(INPUT, 399999).sumOf { row -> row.count { it == '.' } })
    }
}