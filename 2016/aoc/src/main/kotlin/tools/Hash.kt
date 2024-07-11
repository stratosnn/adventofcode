package tools

import java.security.MessageDigest
import kotlin.text.Charsets.UTF_8

fun hashString(str: String, algorithm: String): ByteArray =
    MessageDigest.getInstance(algorithm).digest(str.toByteArray(UTF_8))

@OptIn(ExperimentalStdlibApi::class)
fun ByteArray.toHex() = toHexString()

fun hashByteArray(arr: ByteArray, algorithm: String): ByteArray =
    MessageDigest.getInstance(algorithm).digest(arr)