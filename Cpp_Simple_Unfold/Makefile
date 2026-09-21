# Build the C++ 3D/1D unfolding binary (Simple_RooUnfold_SelfContained.py unfold path).
# Requires ROOT (`root-config`) and RooUnfold.
#
#   make                         # unfolding binary
#   make ROOUNFOLD_DIR=/path     # override RooUnfold location
#
# root-config comes from ROOTSYS or PATH (see rootconfig.mk). Conda is not required.

CXX      ?= g++
# Appended after inherited CXXFLAGS because ?= is ignored when CXXFLAGS is already set.
SIDIS5D_CXXFLAGS := -O3 -fno-math-errno -Wall -Wno-unused-parameter -D_LIBCPP_DISABLE_AVAILABILITY
REPO_ROOT := $(abspath ..)
HELPERS_DIR := $(REPO_ROOT)/Cpp_Dedicated_5D_Unfold

include $(HELPERS_DIR)/rootconfig.mk

ROOT_CFLAGS := $(shell $(ROOTCONFIG) --cflags 2>/dev/null)
ROOT_LIBS   := $(shell $(ROOTCONFIG) --libs 2>/dev/null)
ROOT_GLIBS  := $(shell $(ROOTCONFIG) --glibs 2>/dev/null)
ROOT_PREFIX := $(shell $(ROOTCONFIG) --prefix 2>/dev/null)
ROOT_VERSION := $(shell $(ROOTCONFIG) --version 2>/dev/null)

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

BINNING_HDR := $(HELPERS_DIR)/generated/Dedicated_5D_Binning.h
TARGET := Simple_Unfold

.PHONY: all clean check-env

all: $(TARGET)

$(BINNING_HDR):
	@echo "Missing $(BINNING_HDR). Run: python3 ../Generate_Dedicated_5D_Unfold_Cpp_Binning.py"
	@exit 1

check-env:
	@if [ -z "$(ROOT_CFLAGS)" ]; then echo "ERROR: root-config not found. Set ROOTSYS or PATH."; exit 1; fi
	@echo "Using ROOT $(ROOT_VERSION) from $(ROOTCONFIG) (prefix=$(ROOT_PREFIX))"
	@if [ -z "$(ROOUNFOLD_DIR)" ]; then echo "ERROR: RooUnfold not found. Set ROOUNFOLD_DIR."; exit 1; fi
	@if [ ! -d "$(ROOUNFOLD_INC)" ]; then echo "ERROR: RooUnfold includes not found under $(ROOUNFOLD_DIR)"; exit 1; fi
	@echo "Using RooUnfold includes $(ROOUNFOLD_INC) libs $(ROOUNFOLD_LIBDIR)"

$(TARGET): Simple_Unfold.cxx $(HELPERS_DIR)/Dedicated_5D_Unfold_Helpers.h $(BINNING_HDR) check-env
	$(CXX) $(CXXFLAGS) $(SIDIS5D_CXXFLAGS) $(ROOT_CFLAGS) -I. -I$(HELPERS_DIR) -I$(ROOUNFOLD_INC) \
		Simple_Unfold.cxx -o $(TARGET) \
		$(ROOT_GLIBS) $(ROOT_LIBS) -L$(ROOUNFOLD_LIBDIR) -lRooUnfold -Wl,-rpath,$(ROOUNFOLD_LIBDIR) -Wl,-rpath,$(ROOT_PREFIX)/lib

clean:
	rm -f $(TARGET)
