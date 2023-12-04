package main

import (
	"bufio"
	"log"
	"os"
)

// PART 1

// load file `input/1` into a list of strings
// each string is a combination of numbers and letters
// from each string, extract the first and last digit
// and concatenate them into a two digit number
// for example, if the string is `a1sdf234sdf`, the number is `14`

// find the sum of all the numbers

func readInput() []string {
	file, err := os.Open("../../input/1")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var lines []string

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	return lines
}

func firstDigit(s string) int {
	for _, c := range s {
		if c >= '0' && c <= '9' {
			return int(c - '0')
		}
	}
	log.Fatal("No digit found in", s)
	return 0
}

func lastDigit(s string) int {
	for i := len(s) - 1; i >= 0; i-- {
		c := s[i]
		if c >= '0' && c <= '9' {
			return int(c - '0')
		}
	}
	log.Fatal("No digit found in", s)
	return 0
}

func answer1() int {
	inputLines := readInput()
	sum := 0
	for _, line := range inputLines {
		first := firstDigit(line)
		last := lastDigit(line)
		sum += first*10 + last
	}
	return sum
}

// -----------------------------------------------------------------------

// PART 2

// Now consider also numbers spelled out as words
// e.g., two1nine -> 29

var numberWords = map[string]int{
	"zero":  0,
	"one":   1,
	"two":   2,
	"three": 3,
	"four":  4,
	"five":  5,
	"six":   6,
	"seven": 7,
	"eight": 8,
	"nine":  9,
}

var numbers = [10]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

func wordIndex(s string) map[int][]int {
	index := make(map[int][]int)
	// for each key of numberWords, find all the indices of that key in s and add them to index with the value of the key
	for word, number := range numberWords {
		for i := 0; i+len(word) <= len(s); i++ {
			if s[i:i+len(word)] == word {
				index[number] = append(index[number], i)
			}
		}
	}
	return index
}

func numberIndex(s string) map[int][]int {
	index := make(map[int][]int)
	// for each value of numbers, find all the indices of that value in s and add them to index
	for _, number := range numbers {
		for i := 0; i < len(s); i++ {
			if int(s[i]-'0') == number {
				index[number] = append(index[number], i)
			}
		}
	}
	return index
}

func answer2() int {
	sum := 0
	for _, line := range readInput() {
		d1 := wordIndex(line)
		d2 := numberIndex(line)
		// merge d1 and d2 into d1
		for k, v := range d2 {
			d1[k] = append(d1[k], v...)
		}
		var first, last int
		minIndex := len(line)
		maxIndex := 0
		for key, slice := range d1 {
			for _, index := range slice {
				if index <= minIndex {
					minIndex = index
					first = key
				}
				if index >= maxIndex {
					maxIndex = index
					last = key
				}
			}
		}
		sum += first*10 + last
	}
	return sum
}

// -----------------------------------------------------------------------

var correctAnswers = map[int]int{
	1: 54450,
	2: 54265,
}

var answerFuncs = map[int]func() int{
	1: answer1,
	2: answer2,
}

func printAndTest(question int) {
	answer := answerFuncs[question]()
	correctAnswer, ok := correctAnswers[question]
	if ok && answer != correctAnswer {
		log.Fatal("Wrong answer, expected ", correctAnswer, " got ", answer)
	}
	println(answer)
}

func main() {
	// if no arguments, run all answers
	if len(os.Args) == 1 || os.Args[1] == "1" {
		printAndTest(1)
	}
	if len(os.Args) == 1 || os.Args[1] == "2" {
		printAndTest(2)
	}
	if len(os.Args) > 1 && os.Args[1] != "1" && os.Args[1] != "2" {
		println("Give 1 or 2 as argument, or no argument at all")
	}
}
