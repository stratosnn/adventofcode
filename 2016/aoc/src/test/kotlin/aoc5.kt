import kotlinx.coroutines.*
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.channels.ReceiveChannel
import kotlinx.coroutines.channels.SendChannel
import kotlinx.coroutines.channels.produce
import org.junit.jupiter.api.Test
import tools.getResource
import java.security.MessageDigest
import kotlin.text.Charsets.UTF_8


class aoc5 {

    @Test
    fun part1() {
        val prefix = getResource("/5/input.txt").trim()

        runBlocking {
            val seqChannel = produceNumbers()
            val resultChannel = Channel<Pair<Int, String>>()
            repeat(Runtime.getRuntime().availableProcessors() - 1) {
                hashChecker(prefix, seqChannel, resultChannel)
            }
            val result = buildList {
                for (i in 0..7) {
                    add(resultChannel.receive())
                }
            }
            coroutineContext.cancelChildren()

            result.sortedBy { it.first }
                .joinToString("") { it.second[5].toString() }
                .let { println(it) }
        }
    }

    @Test
    fun part2() {
        val prefix = getResource("/5/input.txt").trim()
        val password = List(8) { ' ' }.toMutableList()

        runBlocking {
            val seqChannel = produceNumbers()
            val resultChannel = Channel<Pair<Int, String>>()
            repeat(Runtime.getRuntime().availableProcessors() + 2) {
                hashChecker(prefix, seqChannel, resultChannel)
            }
            while (password.any { it == ' ' }) {
                val hash = resultChannel.receive().second
                if (hash[5].isDigit() && hash[5].digitToInt() < 8 && password[hash[5].digitToInt()] == ' ') {
                    password[hash[5].digitToInt()] = hash[6]
                }
            }

            coroutineContext.cancelChildren()
        }
        println(password.joinToString(""))
    }

}

fun hashString(str: String, algorithm: String): ByteArray =
    MessageDigest.getInstance(algorithm).digest(str.toByteArray(UTF_8))

fun ByteArray.toHex() = joinToString("") { byte -> "%02x".format(byte) }

@OptIn(ExperimentalCoroutinesApi::class)
fun CoroutineScope.produceNumbers() = produce(capacity = Runtime.getRuntime().availableProcessors() * 16  ) {
    for (seq in 0..Int.MAX_VALUE) {
        send(seq)
    }
}

fun CoroutineScope.hashChecker(
    prefix: String,
    receiveChannel: ReceiveChannel<Int>,
    resultChannel: SendChannel<Pair<Int, String>>
) = launch(Dispatchers.Default) {
    for (seq in receiveChannel) {
        val hash = hashString("$prefix$seq", "MD5").toHex()
        if (hash.startsWith("00000")) {
            resultChannel.send(seq to hash)
        }
    }
}
