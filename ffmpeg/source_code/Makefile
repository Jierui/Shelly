cc=g++
INC=-I/usr/local/include/opencv4
CFLAGS=-g -std=c++11 $(INC)


demo1: demo/main.cpp
	$(cc) $(CFLAGS) `pkg-config --libs opencv` -lavcodec -lavformat -lswscale -lavutil $^ -o $@

push: demo/push.cpp
	$(cc) $(CFLAGS) -lavcodec -lavformat -lswscale -lavutil $^ -o $@