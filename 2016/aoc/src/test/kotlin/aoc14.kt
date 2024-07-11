import org.junit.jupiter.api.Test
import tools.hashString
import tools.toHex
import kotlin.test.assertEquals


class aoc14 {
//    val salt = "abc"
    val salt = "qzyelonm"

    fun String.consecutiveChars(n: Int) =
        (0..length - n).mapNotNull { ix ->
            this[ix].takeIf { (ix+1..<ix+n).all { this[ix] == this[it] } }
        }.toSet()

    fun String.firstConsecutiveChar(n: Int) =
        (0..length - n).firstNotNullOfOrNull { ix ->
            this[ix].takeIf { (ix + 1..<ix + n).all { this[ix] == this[it] } }
        }

    @OptIn(ExperimentalStdlibApi::class)
    fun rehashString(str: String, n: Int) = hashString(str, "MD5").let {
        var result = it
        repeat(n) {
            result = hashString(result.toHexString(), "MD5")
        }
        result.toHexString()
    }

    @Test
    fun `Returns chars that repeat n times`() {
        assertEquals(2, "111222".consecutiveChars(3).size)
        assertEquals(2, "111casdcasdasdef4ag421ff222".consecutiveChars(3).size)
        assertEquals(0, "asdcasdc1_1asdef4ag421ff2_2".consecutiveChars(3).size)
        assertEquals(1, "asdcasdc1_1asdef4ag42122222".consecutiveChars(5).size)
        assertEquals(1, "3aeeeee1367614f3061d165a5fe3cac3".consecutiveChars(5).size)
    }

    @Test
    fun `Rehashing test`() {
        assertEquals("577571be4de9dcce85a041ba0410f29f", rehashString("abc0", 0))
        assertEquals("eec80a0c92dc8a0777c619d9bb51e910", rehashString("abc0", 1))
    }

    @Test
    fun part1() {
        generateSequence(0) { it + 1 }
            .map { it to hashString("$salt$it", "MD5").toHex() }
            .windowed(1001)
            .mapNotNull { hashes ->
                hashes.first()
                    .let { (ix, hash) -> hash.firstConsecutiveChar(3)?.let { ix to it } }
                    ?.takeIf { (_, triple) ->
                        hashes.drop(1)
                            .firstNotNullOfOrNull { (_, hash) ->
                                hash.consecutiveChars(5)
                                    .takeIf { it.isNotEmpty() }
                                    ?.any { it == triple }
                                    ?.takeIf { it }
                            } == true
                    }?.first // here we return ix of the hash if it has consecutive 5 chars in the next 1000
            }.take(64)
            .toList()
            .let { println(it.last()) }

    }

    @Test
    fun part2() {
        generateSequence(0) { it + 1 }
            .map { it to rehashString("$salt$it", 2016) }
            .windowed(1001)
            .mapNotNull { hashes ->
                hashes.first()
                    .let { (ix, hash) -> hash.firstConsecutiveChar(3)?.let { ix to it } }
                    ?.takeIf { (_, triple) ->
                        hashes.drop(1)
                            .firstNotNullOfOrNull { (_, hash) ->
                                hash.consecutiveChars(5)
                                    .takeIf { it.isNotEmpty() }
                                    ?.any { it == triple }
                                    ?.takeIf { it }
                            } == true
                    }?.first // here we return ix of the hash if it has consecutive 5 chars in the next 1000
            }.take(64)
            .toList()
            .let { println(it.last()) }
    }
}
