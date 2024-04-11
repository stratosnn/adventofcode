package org.example.tools

tailrec fun Long.gcd(b: Long): Long = if (b == 0L) this else b.gcd(this % b)

fun Long.lcm(b: Long) = this * b / this.gcd(b)


tailrec fun Int.gcd(b: Int): Int = if (b == 0) this else b.gcd(this % b)

fun Int.lcm(b: Int) = this * b / this.gcd(b)