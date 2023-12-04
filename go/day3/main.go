package main

import (
	"bufio"
	"log"
	"os"
)

// PART 1

// Your input is like this:

// 467..114..
// ...*......
// ..35..633.

// Sum all the numbers not adjacent (even diagonally) to a symbol,
// except for dots (.), in this case 114+633=747

func readInput() []string {
	file, err := os.Open("../../input/3")
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

// maxY and maxX are the number of lines and columns in the grid
type world struct {
	grid []string
	maxY int
	maxX int
}

func theWorld() world {
	lines := readInput()
	return world{lines, len(lines), len(lines[0])}
}

// pos represent a position in the grid, starting at 0,0
// in the top left corner, with x going right and y going down
type pos struct {
	x, y int
}

// all the numbers in the grid, with their value and the
// positions of all the digits
type number struct {
	value     int
	positions []pos
}

// numbers returns a slice of alll the numbers in the grid
func numbers(w *world) []number {
	var numbers []number
	for y, line := range w.grid {
		var readingNumber bool
		var n int
		var positions []pos
		for x, char := range line {
			if char >= '0' && char <= '9' {
				if !readingNumber {
					readingNumber = true
				}
				n = n*10 + int(char-'0')
				positions = append(positions, pos{x, y})
				if x == w.maxX-1 {
					numbers = append(numbers, number{n, positions})
				}
			} else {
				if readingNumber {
					numbers = append(numbers, number{n, positions})
					readingNumber = false
					n = 0
					positions = nil
				}
			}
		}
	}
	return numbers
}

// isSymbol returns true if the given character is not a digit nor a dot
func isSymbol(char rune) bool {
	return char != '.' && (char < '0' || char > '9')
}

// neighbors returns a slice of all the positions of the neighbors of
// the given position, excluding negative positions or positions
// over the maximum x or y
func neighbors(p pos, w *world) []pos {
	var positions []pos
	for _, neighbor := range []pos{
		{p.x - 1, p.y - 1}, // top left
		{p.x, p.y - 1},     // top
		{p.x + 1, p.y - 1}, // top right
		{p.x - 1, p.y},     // left
		{p.x + 1, p.y},     // right
		{p.x - 1, p.y + 1}, // bottom left
		{p.x, p.y + 1},     // bottom
		{p.x + 1, p.y + 1}, // bottom right
	} {
		if neighbor.x >= 0 && neighbor.y >= 0 &&
			neighbor.x < w.maxX && neighbor.y < w.maxY {
			positions = append(positions, neighbor)
		}
	}
	return positions
}

func isAdjacentToSymbol(n *number, w *world) bool {
	for _, p := range n.positions {
		for _, neighbor := range neighbors(p, w) {
			if isSymbol(rune(w.grid[neighbor.y][neighbor.x])) {
				return true
			}
		}
	}
	return false
}

func answer1() int {
	w := theWorld()
	numbers := numbers(&w)
	var sum int
	for _, n := range numbers {
		if isAdjacentToSymbol(&n, &w) {
			sum += n.value
		}
	}
	return sum
}

// -----------------------------------------------------------------------

// PART 2

// each `*` adjacent to exactly 2 numbers is a `gear`. Find all gears
// and sum their `gear ratio` which is the product of the 2 adjacent numbers
func isDigit(char byte) bool {
	return rune(char) >= '0' && rune(char) <= '9'
}

// find the number with a digit in the given position
// inefficient for large dataset, you would scan the grid
// directly around the position instead
func findNumberAt(x, y int, ns []number) int {
	for _, n := range ns {
		for _, p := range n.positions {
			if p.x == x && p.y == y {
				return n.value
			}
		}
	}
	return 0
}
func gearRatios(w *world, ns []number) int {
	var sum int
	for y, line := range w.grid {
		for x, char := range line {
			if char == '*' {
				var countNumbers int
				product := 1
				// check left
				if x > 0 && isDigit(w.grid[y][x-1]) {
					countNumbers++
					if countNumbers == 3 {
						continue
					}
					product *= findNumberAt(x-1, y, ns)
				}
				// check right
				if x < w.maxX-1 && isDigit(w.grid[y][x+1]) {
					countNumbers++
					if countNumbers == 3 {
						continue
					}
					product *= findNumberAt(x+1, y, ns)
				}
				// check top
				if y > 0 {
					// if straight above is a number then only one number on top
					if isDigit(w.grid[y-1][x]) {
						countNumbers++
						if countNumbers == 3 {
							continue
						}
						product *= findNumberAt(x, y-1, ns)
					} else {
						// check top left
						if x > 0 && isDigit(w.grid[y-1][x-1]) {
							countNumbers++
							if countNumbers == 3 {
								continue
							}
							product *= findNumberAt(x-1, y-1, ns)
						}
						// check top right
						if x < w.maxX-1 && isDigit(w.grid[y-1][x+1]) {
							countNumbers++
							if countNumbers == 3 {
								continue
							}
							product *= findNumberAt(x+1, y-1, ns)
						}
					}
				}
				// check bottom
				if y < w.maxY-1 {
					// if straight below is a number then only one number below
					if isDigit(w.grid[y+1][x]) {
						countNumbers++
						if countNumbers == 3 {
							continue
						}
						product *= findNumberAt(x, y+1, ns)
					} else {
						// check bottom left
						if x > 0 && isDigit(w.grid[y+1][x-1]) {
							countNumbers++
							if countNumbers == 3 {
								continue
							}
							product *= findNumberAt(x-1, y+1, ns)
						}
						// check bottom right
						if x < w.maxX-1 && isDigit(w.grid[y+1][x+1]) {
							countNumbers++
							if countNumbers == 3 {
								continue
							}
							product *= findNumberAt(x+1, y+1, ns)
						}
					}
				}
				if countNumbers == 2 {
					sum += product
				}
			}
		}
	}
	return sum
}

func answer2() int {
	w := theWorld()
	return gearRatios(&w, numbers(&w))
}

// -----------------------------------------------------------------------

var correctAnswers = map[int]int{
	1: 543867,
	2: 79613331,
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
