CC = g++
CFLAGS = -std=c++17
SRC = main.cpp utils/utils.cpp utils/algorithms.cpp
OBJ = $(SRC:.cpp=.o)
EXEC = pwl_fit

all: $(EXEC)

$(EXEC): $(OBJ)
	$(CC) $(OBJ) -o $(EXEC)

%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

main.o: main.cpp utils/utils.h utils/algorithms.h

utils/utils.o: utils/utils.cpp utils/utils.h

utils/algorithms.o: utils/algorithms.cpp utils/algorithms.h

clean:
	rm -f $(OBJ) $(EXEC)
