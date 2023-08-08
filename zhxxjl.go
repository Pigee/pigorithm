package main

import (
	"encoding/csv"
	"fmt"
	"github.com/gocarina/gocsv"
	"github.com/shopspring/decimal"
	"io"
	"math/rand"
	"os"
	"sort"
	"strconv"
	"time"
)

// https://stackoverflow.com/questions/23121026/how-to-sort-by-time-time
// https://github.com/gocarina/gocsv
// https://zhidao.baidu.com/question/1373065820887869539.html
//  (关于excel保存为csv格式后，重新打开文本型数字变为科学计数，且15位后面变成0)

type Zhxx struct {
	Id        string
	Ed        float64
	Zhtime    time.Time
	Ye        float64
	Zhtimestr string
}
type xxSlice []Zhxx

func (xs xxSlice) Randomxx(t time.Time) Zhxx {
	var rxx xxSlice
	for _, x := range xs {
		if x.Ye > 0 && t.After(x.Zhtime) {
			rxx = append(rxx, x)
		}
	}
	return rxx[rand.Intn(len(rxx))]
}

func (xs xxSlice) Updateye(id string, e float64) {
	for i, item := range xs {
		if item.Id == id {
			if xs[i].Ye > e {
				xs[i].Ye, _ = decimal.NewFromFloat(xs[i].Ye - e).Round(2).Float64()
			} else {
				xs[i].Ye = 0
			}
			return
		}
	}
}

type Zhjl struct {
	Ck        float64
	Cktime    time.Time
	Zhid      string
	Ye        float64
	Cktimestr string
}
type jlSlice []Zhjl

func (p jlSlice) Len() int {
	return len(p)
}

func (p jlSlice) Less(i, j int) bool {
	return p[i].Cktime.Before(p[j].Cktime)
}

func (p jlSlice) Swap(i, j int) {
	p[i], p[j] = p[j], p[i]
}

// Time Format
type DateTime struct {
	time.Time
}

// Convert the internal date as CSV string
func (date *DateTime) MarshalCSV() (string, error) {
	return date.Time.Format("2006-01-02 15:04:05"), nil
}

// Main Logic start Here....
func main() {
	jl := getZhjl("zhjl.csv")
	zh := getZhxx("zhxx.csv")

	var zhjl_exp jlSlice
	// i := 0
	for _, jlone := range jl {
		jlck := jlone.Ck //loop for record to be consumed...
		for jlck > 0 {
			zhye := zh.Randomxx(jlone.Cktime)

			if jlck > zhye.Ye {
				jlone.Ck = zhye.Ye
				jlone.Zhid = zhye.Id
				jlone.Cktimestr = jlone.Cktime.Format("2006-01-02 15:04:05")
				jlone.Ye = 0
				fmt.Println(jlone)
				zhjl_exp = append(zhjl_exp, jlone)
				jlone.Ck, _ = decimal.NewFromFloat(jlck - zhye.Ye).Round(2).Float64()
			} else {
				jlone.Ye, _ = decimal.NewFromFloat(zhye.Ye - jlck).Round(2).Float64()
				jlone.Zhid = zhye.Id
				jlone.Cktimestr = jlone.Cktime.Format("2006-01-02 15:04:05")

				fmt.Println(jlone)
			  zhjl_exp = append(zhjl_exp, jlone)
			}

			zh.Updateye(zhye.Id, jlck) // Update zh Slice
			fmt.Println(zhye)
			fmt.Println("Done.............................")
			jlck = jlck - zhye.Ye
		}
		/*
		   if i > 10 {
		   break
		   }
		   i++
		*/
	}
	// Write to CSV file

	jlFile, err := os.OpenFile("zhjl_exp.csv", os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		panic(err)
	}
	defer jlFile.Close()
	gocsv.MarshalFile(&zhjl_exp, jlFile)

	xxFile, err := os.OpenFile("zhxx_exp.csv", os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		panic(err)
	}
	defer xxFile.Close()
	gocsv.MarshalFile(&zh, xxFile)

	/*
	   csvContent, err := gocsv.MarshalString(&zh_exp)
	   if err != nil {
	   panic(err)
	   }
	   fmt.Println(csvContent)
	*/

	//fmt.Println(zh_exp)
	// writeJl("zhxx_exp.csv",zh_exp)

}

// Parse account info and return xxSlice

func getZhxx(f string) xxSlice {
	timeFormat := "2006-01-02 15:04:05"
	var LOC, err = time.LoadLocation("Asia/Shanghai")
	if err != nil {
		LOC = time.FixedZone("CST", 8*3600) //替换上海时区
	}
	var xxslice xxSlice
	var xx Zhxx

	file, err := os.Open(f)
	if err != nil {
		panic(err)
	}

	defer file.Close()
	reader := csv.NewReader(file)
	i := 0 // Skip the first header row
	for {
		record, err := reader.Read()

		if err == io.EOF {
			break
		}

		if err != nil {
			panic(err)
		}
		if i > 0 {
			xx.Id = record[0]
			// fmt.Println(record[0])
			xx.Ed, _ = strconv.ParseFloat(record[1], 64)
			xx.Zhtime, _ = time.ParseInLocation(timeFormat, record[2], LOC)
			xx.Ye, _ = strconv.ParseFloat(record[1], 64)
			xx.Zhtimestr = xx.Zhtime.Format("2006-01-02 15:04:05")
			xxslice = append(xxslice, xx)
		}
		i++
		// fmt.Println(record)
		// break
	}

	return xxslice
	// fmt.Println(xxslice)

}

// Parse Record slice info and return Slice

func getZhjl(f string) jlSlice {
	timeFormat := "2006-01-02 15:04:05"
	var LOC, err = time.LoadLocation("Asia/Shanghai")
	if err != nil {
		LOC = time.FixedZone("CST", 8*3600) //替换上海时区
	}
	var jlslice jlSlice
	var jl Zhjl

	file, err := os.Open(f)
	if err != nil {
		panic(err)
	}

	defer file.Close()
	reader := csv.NewReader(file)
	i := 0 // Skip the first header row
	for {
		record, err := reader.Read()

		if err == io.EOF {
			break
		}

		if err != nil {
			panic(err)
		}

		if i > 0 {
			jl.Ck, _ = strconv.ParseFloat(record[0], 64)
			jl.Cktime, _ = time.ParseInLocation(timeFormat, record[1], LOC)
			// jl.Ye, _ = strconv.ParseFloat(record[1], 64)
			jlslice = append(jlslice, jl)
		}
		// fmt.Println(record)
		// break
		i++
	}
	sort.Sort(jlslice)
	return jlslice

}
