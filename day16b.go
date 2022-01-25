package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

var basePattern = []int64{0, 1, 0, -1}

func main() {
	inputLine := strings.TrimSpace(<-inputLines())
	inputDigits := []int64{}
	for i := 0; i < len(inputLine); i++ {
		x, _ := strconv.Atoi(inputLine[i:i+1])
		inputDigits = append(inputDigits, int64(x))
	}
	m := len(inputDigits)

	repeats := 10000

	signal := make([]int64, len(inputDigits) * repeats)
	for i := 0; i < repeats; i++ {
		copy(signal[i * m:(i+1)*m], inputDigits)
	}
	n := len(signal)

	for phase := 0; phase < 100; phase++ {
		cum := make([]int64, len(signal))
		cum[0] = signal[0]
		for i := 1; i < len(signal); i++ {
			cum[i] = cum[i-1] + signal[i]
		}

		outSignal := make([]int64, n)
		for outIndex := 0; outIndex < n; outIndex++ {
			blockSize := outIndex + 1
			patternIndex := 0
			i := -1
			s := int64(0)
			for i < n {
				c := basePattern[patternIndex]
				if c != 0 {
					var blockSum int64
					if blockSize == 1 {
						blockSum = signal[i]
					} else {
						j := min(n - 1, i + blockSize - 1)
						blockSum = cum[j] - cum[i - 1]
					}
					s += c * blockSum
				}
				i += blockSize
				patternIndex = (patternIndex + 1) % len(basePattern)
			}
			outSignal[outIndex] = abs(s) % 10
		}

		signal = outSignal
	}

	offset, _ := strconv.Atoi(inputLine[:7])
	message := signal[offset:offset+8]
	for _, d := range message {
		fmt.Print(d)
	}
	fmt.Println()
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func abs(a int64) int64 {
	if a < 0 {
		return -a
	} 
	return a
}

func inputLines() <-chan string {
	ch := make(chan string)

	go func() {
		inFile, err := os.Open(os.Args[1])
		if err != nil {
			log.Fatal(err)
		}

		scanner := bufio.NewScanner(inFile)
		for scanner.Scan() {
			line := scanner.Text()
			ch <- line
		}
		if err := scanner.Err(); err != nil {
			log.Fatal(err)
		}

		close(ch)
	}()

	return ch
}
