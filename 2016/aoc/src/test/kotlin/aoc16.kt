import kotlin.test.Test
import kotlin.test.assertEquals


class aoc16 {

    fun String.toBooleanArray() = this.map {
        when(it) {
            '1' -> true
            '0' -> false
            else -> error("Unexpected character $it")
        }
    }.toBooleanArray()

    fun BooleanArray.stringify() = joinToString("") { if (it) { "1" } else { "0" } }

    val input = "01110110101001000".toBooleanArray()

    fun expand(arr: BooleanArray): BooleanArray {
        val transformed = arr.reversed().map { !it }.toBooleanArray()
        return BooleanArray(2*arr.size + 1) { ix ->
            if (ix < arr.size) {
                arr[ix]
            } else if (ix == arr.size) {
                false
            } else {
                transformed[ix - arr.size - 1]
            }
        }
    }

    fun expandUntil(arr: BooleanArray, desiredSize: Int): BooleanArray {
        var res = arr
        while (res.size < desiredSize) {
            res = expand(res)
        }
        return res
    }

    fun fold(arr: BooleanArray) = arr.toList().chunked(2).map { (first, second) -> first == second }.toBooleanArray()

    fun checksum(arr: BooleanArray): BooleanArray {
        var res = arr
        while (res.size % 2 == 0) {
            res = fold(res)
        }
        return res
    }


    @Test
    fun `It can expand data correctly`() {
        assertEquals("1111000010100101011110000", "111100001010".toBooleanArray().let { expand(it) }.stringify())
    }

    @Test
    fun `It can checksum data correctly`() {
        assertEquals("01100", "10000011110010000111".toBooleanArray().let { checksum(it) }.stringify())
    }

    @Test
    fun part1() {
        val data = expandUntil(input, 272).take(272).toBooleanArray()
        println(checksum(data).stringify())
    }

    @Test
    fun part2() {
        val data = expandUntil(input, 35651584).take(35651584).toBooleanArray()
        println(checksum(data).stringify())
    }
}