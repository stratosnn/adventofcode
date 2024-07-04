import org.junit.jupiter.api.Test
import tools.getResourceAsStrings


class aoc4 {

    data class Room(
        val segments: List<String>,
        val sectorId: Int,
        val checksum: String
    )

    fun parseInput(fileName: String) = getResourceAsStrings(fileName).map { line ->
        val rawSegments = line.split("-")
        val (sectorId, checksum) = rawSegments.last().split('[', ']').filterNot { it.isEmpty() }
        Room(rawSegments.dropLast(1), sectorId.toInt(), checksum)
    }

    fun isRealRoom(room: Room) =
        room.segments
            .joinToString("")
            .groupingBy { it }
            .eachCount()
            .asSequence()
            .sortedWith(compareBy({ -it.value }, { it.key }))
            .map { it.key }
            .take(5)
            .joinToString("") == room.checksum

    @Test
    fun part1() {
        parseInput("/4/input.txt")
            .filter { room -> isRealRoom(room) }
            .sumOf { it.sectorId }
            .let { println(it) }
    }

    @Test
    fun part2() {
        parseInput("/4/input.txt")
            .filter { room -> isRealRoom(room) }
            .map { room ->
                val name = room.segments.map {
                    it.map { c -> 'a' + (c - 'a' + room.sectorId) % 26 }.joinToString("")
                }
                Room(name, room.sectorId, room.checksum)
            }.filter {
                it.segments.contains("northpole")
            }.let {
                println(it)
            }
    }

}