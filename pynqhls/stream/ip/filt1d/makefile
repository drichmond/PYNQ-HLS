TARGET=filt1d

all: $(TARGET)

$(TARGET): $(TARGET).cpp main.cpp
	vivado_hls -f generate.tcl

clean:
	rm -rf *.log *.jou $(TARGET)
