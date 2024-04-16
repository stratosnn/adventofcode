package aoc

import org.example.tools.getResource
import kotlin.test.Test
import kotlin.test.assertEquals

class aoc15 {

    private fun hash(input: String) = input.fold(0) { acc, c -> (17 * (acc + c.code)) % 256 }

    @Test
    fun testHashFunction() {
        assertEquals(52, hash("HASH"))
    }

    @Test
    fun part1() {
        val result = getResource("/15/input.txt")
            .trim()
            .split(',')
            .sumOf { hash(it) }
        println(result)
    }

    @Test
    fun part2() {
        val commands = getResource("/15/input.txt")
            .trim()
            .split(',')

        val boxes = List(256) { mutableListOf<Pair<String, Int>>() }

        commands.forEach { command ->
            val cmdSplit = command.split('-', '=')
            val label = cmdSplit.first()
            when {
                command.contains('-') -> {
                    val box = boxes[hash(label)]
                    box.firstOrNull { it.first == label }
                        ?.let { box.remove(it) }
                }

                command.contains('=') -> {
                    val focal = cmdSplit[1].toInt()
                    val box = boxes[hash(label)]
                    box.indexOfFirst { it.first == label }
                        .takeIf { it >= 0 }
                        ?.let { box[it] = label to focal }
                        ?: box.add(label to focal)
                }
            }
        }

        val result = boxes.foldIndexed(0L) { boxIx, acc, box ->
            acc + box.foldIndexed(0L) { lensIx, boxAcc, lens ->
                boxAcc + ((boxIx + 1) * (lensIx + 1) * lens.second)
            }
        }

        println(result)

    }
}