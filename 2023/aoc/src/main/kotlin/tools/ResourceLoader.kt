package org.example.tools

class ResourceLoader

fun getResource(path: String) =
    ResourceLoader::class.java.getResourceAsStream(path)?.bufferedReader()?.readText()
        ?: throw IllegalArgumentException("File $path is not found")
fun getResourceAsStrings(path: String) =
    ResourceLoader::class.java.getResourceAsStream(path)?.bufferedReader()?.readLines()
        ?: throw IllegalArgumentException("File $path is not found")