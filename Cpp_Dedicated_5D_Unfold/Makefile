# Build the C++ Dedicated 5D unfolding binary.
# Requires ROOT (`root-config`) and RooUnfold.
#
#   make                         # unfolding binary
#   make binning_check           # no ROOT / RooUnfold
#   make ROOUNFOLD_DIR=/path     # override RooUnfold location

CXX      ?= g++
CXXFLAGS ?= -O2 -std=c++14 -Wall -Wno-unused-parameter
REPO_ROOT := $(abspath ..)

ROOTCONFIG ?= $(shell command -v root-config 2>/dev/null)
ifeq ($(ROOTCONFIG),)
  ROOTCONFIG := $(ROOTSYS)/bin/root-config
endif

ROOT_CFLAGS := $(shell $(ROOTCONFIG) --cflags 2>/dev/null)
ROOT_LIBS   := $(shell $(ROOTCONFIG) --libs 2>/dev/null)
ROOT_GLIBS  := $(shell $(ROOTCONFIG) --glibs 2>/dev/null)

# Prefer a RooUnfold tree that actually contains headers.
define pick_roounfold
$(firstword $(foreach d,$(1),$(if $(wildcard $(d)/src/RooUnfoldResponse.h)$(wildcard $(d)/include/RooUnfoldResponse.h)$(wildcard $(d)/RooUnfoldResponse.h),$(d),)))
endef
ROOUNFOLD_CANDIDATES := $(ROOUNFOLD_DIR) \
  $(REPO_ROOT)/New_RooUnfold/RooUnfold \
  /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold \
  /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/New_RooUnfold/RooUnfold
ROOUNFOLD_DIR := $(call pick_roounfold,$(ROOUNFOLD_CANDIDATES))

define find_roounfold_inc
$(firstword $(wildcard \
  $(1)/src \
  $(1)/build/src \
  $(1)/include \
  $(1)))
endef
define find_roounfold_libdir
$(firstword $(wildcard \
  $(1)/build \
  $(1)/build/lib \
  $(1)/lib \
  $(1)))
endef

ROOUNFOLD_INC := $(call find_roounfold_inc,$(ROOUNFOLD_DIR))
ROOUNFOLD_LIBDIR := $(call find_roounfold_libdir,$(ROOUNFOLD_DIR))

BINNING_HDR := generated/Dedicated_5D_Binning.h
TARGET := Dedicated_5D_Unfold

.PHONY: all clean check-env binning_check

all: $(TARGET)

$(BINNING_HDR):
	@echo "Missing $(BINNING_HDR). Run: python3 ../Generate_Dedicated_5D_Unfold_Cpp_Binning.py"
	@exit 1

check-env:
	@if [ -z "$(ROOT_CFLAGS)" ]; then echo "ERROR: root-config not found. Set ROOTSYS or PATH."; exit 1; fi
	@if [ -z "$(ROOUNFOLD_DIR)" ]; then echo "ERROR: RooUnfold not found. Set ROOUNFOLD_DIR."; exit 1; fi
	@if [ ! -d "$(ROOUNFOLD_INC)" ]; then echo "ERROR: RooUnfold includes not found under $(ROOUNFOLD_DIR)"; exit 1; fi

$(TARGET): Dedicated_5D_Unfold.cxx Dedicated_5D_Unfold_Helpers.h $(BINNING_HDR) check-env
	$(CXX) $(CXXFLAGS) $(ROOT_CFLAGS) -I. -I$(ROOUNFOLD_INC) \
		Dedicated_5D_Unfold.cxx -o $(TARGET) \
		$(ROOT_GLIBS) $(ROOT_LIBS) -L$(ROOUNFOLD_LIBDIR) -lRooUnfold -Wl,-rpath,$(ROOUNFOLD_LIBDIR)

binning_check: binning_check.cxx $(BINNING_HDR)
	$(CXX) $(CXXFLAGS) -I. binning_check.cxx -o $@

clean:
	rm -f $(TARGET) binning_check
