my.o : my.h my.cpp
	g++ -c my.cpp

main.o : my.h main.cpp
	g++ -c main.cpp


test : my.o main.o
	g++ -o test main.o my.o

all : test

clear :
	rm -f my.o main.o test
