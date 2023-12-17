package main

import (
	"bufio"
	"crypto/sha256"
	"encoding/hex"
	"io"
	"log"
	"os"
)

// PART 1

// You input is like the following:

// O....#....
// O.OO#....#
// .....##...
// OO.#O....O
// .O.....O#.
// O.#..O.#.#
// ..O..#O..O
// .......O..
// #....###..
// #OO..#....

// 'O' are rolling rocks, '#' are fixed rocks, '.' are open spaces.
// Start by tilting the board north so that all rolling rocks roll
// north as much as possible (fixed rocks will not move).
// THen sum the "load" of each rolling rock, which is the index of the row
// it is on, where the southmost row is 1 and it increases by 1 for each row.

func readInput() [][]byte {
	file, err := os.Open("../../input/14")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	var columns [][]byte
	i := 0
	columns = append(columns, []byte{})
	// read bytes from reader into columns
	for {
		newByte, err := reader.ReadByte()
		if err == io.EOF {
			break
		}
		if newByte == '\n' {
			i = 0
			continue
			columns = append(columns, []byte{})
		} else {
			columns[i] = append(columns[i], newByte)
			i++
			if i >= len(columns) {
				columns = append(columns, []byte{})
			}
		}
	}
	if len(columns[len(columns)-1]) == 0 {
		columns = columns[:len(columns)-1]
	}
	return columns
}

func tiltColumnNorth(column []byte) []int {
	// tilt the column north and return a list of positions of rolling rocks
	// as index of the row they are on, where the northmost row is 0.
	rolling := []int{}
	empty := []int{}
	for i, c := range column {
		if c == 'O' {
			if len(empty) > 0 {
				rolling = append(rolling, empty[0])
				empty = empty[1:]
				empty = append(empty, i)
			} else {
				rolling = append(rolling, i)
			}
		} else if c == '.' {
			empty = append(empty, i)
		} else { //  c == '#'
			empty = []int{}
		}
	}
	return rolling
}

func columnLoadFromPositions(rolling []int, lenCol int) int {
	// calculate the load of a list of rolling rocks positions.
	// where the northmost row is lenCol and the southmost row is 1.
	sum := 0
	for _, r := range rolling {
		sum += lenCol - r
	}
	return sum
}

func answer1() int {
	columns := readInput()
	sum := 0
	lenCol := len(columns[0])
	for _, col := range columns {
		sum += columnLoadFromPositions(tiltColumnNorth(col), lenCol)
	}
	return sum
}

// -----------------------------------------------------------------------

// PART 2

// Now you need to complete 1000000000 cycles of rolling before calculating
// the load of the rolling rocks.
// Each cycle is a tilt north, west, south and east in that order.

func tiltWest(columns [][]byte) {
	// tilt the columns west
	for x := 0; x < len(columns[0]); x++ {
		empty := []int{}
		for y := 0; y < len(columns); y++ {
			c := columns[y][x]
			if c == 'O' {
				if len(empty) > 0 {
					columns[empty[0]][x] = 'O'
					empty = empty[1:]
					empty = append(empty, y)
					columns[y][x] = '.'
				}
			} else if c == '.' {
				empty = append(empty, y)
			} else { //  c == '#'
				empty = []int{}
			}
		}
	}
}

func tiltEast(columns [][]byte) {
	// tilt the columns east
	for x := 0; x < len(columns[0]); x++ {
		empty := []int{}
		for y := len(columns) - 1; y >= 0; y-- {
			c := columns[y][x]
			if c == 'O' {
				if len(empty) > 0 {
					columns[empty[0]][x] = 'O'
					empty = empty[1:]
					empty = append(empty, y)
					columns[y][x] = '.'
				}
			} else if c == '.' {
				empty = append(empty, y)
			} else { //  c == '#'
				empty = []int{}
			}
		}
	}
}

func tiltNorth(columns [][]byte) {
	// tilt the columns north
	for _, col := range columns {
		empty := []int{}
		for x, c := range col {
			if c == 'O' {
				if len(empty) > 0 {
					col[empty[0]] = 'O'
					empty = empty[1:]
					empty = append(empty, x)
					col[x] = '.'
				}
			} else if c == '.' {
				empty = append(empty, x)
			} else { //  c == '#'
				empty = []int{}
			}
		}
	}
}

func tiltSouth(columns [][]byte) {
	// tilt the columns south
	for _, col := range columns {
		empty := []int{}
		for x := len(col) - 1; x >= 0; x-- {
			c := col[x]
			if c == 'O' {
				if len(empty) > 0 {
					col[empty[0]] = 'O'
					empty = empty[1:]
					empty = append(empty, x)
					col[x] = '.'
				}
			} else if c == '.' {
				empty = append(empty, x)
			} else { //  c == '#'
				empty = []int{}
			}
		}
	}
}

func load(columns [][]byte) int {
	// calculate the load of the board
	sum := 0
	lenCol := len(columns[0])
	for _, col := range columns {
		for i, c := range col {
			if c == 'O' {
				sum += lenCol - i
			}
		}
	}
	return sum
}

//func printBoard(columns [][]byte) {
//for x := range columns[0] {
//for y := range columns {
//fmt.Print(string(columns[y][x]))
//}
//fmt.Println()
//}
//fmt.Println()
//}

func performCycle(columns [][]byte) {
	// perform a cycle on the board
	tiltNorth(columns)
	tiltWest(columns)
	tiltSouth(columns)
	tiltEast(columns)
}

// hashBytesSlice hashes a [][]byte and returns a hex string representation.
func hashBytesSlice(data [][]byte) string {
	hasher := sha256.New()
	for _, b := range data {
		hasher.Write(b)
	}
	return hex.EncodeToString(hasher.Sum(nil))
}

func findRepeatCycle(columns [][]byte, maxCycles int) (int, int) {
	// Get a board and perform up to maxCycles cycles looking for a repeated configuration.
	// Return: number of cycles to first reach it and number of cycles to then repeat it
	// If no repeated configuration is found, return 0, 0
	patterns := map[string]int{}
	for i := 0; i < maxCycles; i++ {
		hash := hashBytesSlice(columns)
		if start, ok := patterns[hash]; ok {
			return start, i - start
		}
		patterns[hash] = i
		performCycle(columns)
	}
	return 0, 0
}

func answer2() int {
	columns := readInput()
	cyclesToPattern, repeatLen := findRepeatCycle(columns, 1000)
	if repeatLen == 0 {
		log.Fatal("No repeated configuration found")
	}
	totalCycles := 1000000000
	cyclesLeft := (totalCycles - cyclesToPattern) % repeatLen
	for i := 0; i < cyclesLeft; i++ {
		performCycle(columns)
	}
	return load(columns)
}

// -----------------------------------------------------------------------

var correctAnswers = map[int]int{
	1: 110821,
	2: 83516,
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
	// if no argument, run all answers, otherwise only part 1 or 2
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
