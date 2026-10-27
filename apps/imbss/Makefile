BUILD_DIR = build
CMAKE_FLAGS = -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=${HOME}/.local
# вариант через nproc
# THREADS ?= $$(nproc)

.PHONY: all configure build clean rebuild run

all: build

configure:
	cmake -B $(BUILD_DIR) -S . $(CMAKE_FLAGS)

build:
	@if [ ! -d "$(BUILD_DIR)" ]; then $(MAKE) configure; fi
# 	cmake --build $(BUILD_DIR) -j$(THREADS)
	cmake --build $(BUILD_DIR) --parallel

clean:
	rm -rf $(BUILD_DIR)

rebuild: clean configure build

run: build
	./$(BUILD_DIR)/imbss


install: build
	cmake --install $(BUILD_DIR) --config Release --strip