package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"runtime"
	"strconv"
	"strings"
)

func main() {
	input := "ckczppom"
	fmt.Println(part1and2(input, "00000"))
	fmt.Println(part1and2(input, "000000"))
}

func GetMD5Hash(text string) string {
	hash := md5.Sum([]byte(text))
	return hex.EncodeToString(hash[:])
}

func part1and2(input, prefix string) int {
	ch := make(chan int, 1024)
	resultChannel := make(chan int)

	for i := 0; i < runtime.NumCPU(); i++ {
		go func() {
			for c := range ch {
				hash := GetMD5Hash(input + strconv.Itoa(c))
				if strings.HasPrefix(hash, prefix) {
					resultChannel <- c
				}
			}
		}()
	}

	cnt := 0

	go func() {
		for {
			ch <- cnt
			cnt++
		}
	}()

	return <-resultChannel
}
