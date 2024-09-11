import org.junit.jupiter.api.Test
import tools.Point2D
import tools.hashString
import tools.toHex


data class Room(
    val point: Point2D,
    val path: String,
)

class aoc17 {

    companion object {
        const val INPUT = "pxxbnzuo"
        const val OPENED_DOORS = "bcdef"
        val STEPS = listOf(
            'U' to Point2D(0, -1),
            'D' to Point2D(0, 1),
            'L' to Point2D(-1, 0),
            'R' to Point2D(1, 0),
        )
        val HASH_OFFSETS = mapOf(
            'U' to 0,
            'D' to 1,
            'L' to 2,
            'R' to 3,
        )
    }

    private fun allowedToBe(room: Room, hash: String) =
        room.point.x in 0..3 && room.point.y in 0..3 && hash[HASH_OFFSETS[room.path.last()]!!] in OPENED_DOORS



    @Test
    fun part1() {
        var pos = Room(Point2D(0, 0), "")
        val vault = Point2D(3, 3)
        val queue = mutableListOf(pos)

        while (queue.isNotEmpty() && pos.point != vault) {
            pos = queue.removeAt(0)
            val hash = hashString("$INPUT${pos.path}", "MD5").toHex().take(4)

            STEPS
                .map { Room(pos.point + it.second, pos.path + it.first) }
                .filter { allowedToBe(it, hash) }
                .forEach { queue.add(it) }
        }

        println(pos.path)
    }

    @Test
    fun part2() {
        var pos = Room(Point2D(0, 0), "")
        val vault = Point2D(3, 3)
        val queue = mutableListOf(pos)
        val possiblePaths = mutableListOf<String>()

        while (queue.isNotEmpty()) {
            pos = queue.removeAt(0)
            if (pos.point == vault) {
                possiblePaths.add(pos.path)
                continue
            }
            val hash = hashString("$INPUT${pos.path}", "MD5").toHex().take(4)

            STEPS
                .map { Room(pos.point + it.second, pos.path + it.first) }
                .filter { allowedToBe(it, hash) }
                .forEach { queue.add(it) }

        }

        println(possiblePaths.maxOfOrNull { it.length })

    }

}