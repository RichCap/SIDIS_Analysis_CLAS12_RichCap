# Find root-config: ROOTCONFIG if set, else ROOTSYS, else CONDA_PREFIX if already set, else PATH. Conda is not required.

define existing_rootconfig
$(if $(1),$(wildcard $(1)/bin/root-config),)
endef

ifeq ($(origin ROOTCONFIG),undefined)
  ROOTCONFIG := $(firstword \
    $(call existing_rootconfig,$(ROOTSYS)) \
    $(call existing_rootconfig,$(CONDA_PREFIX)) \
    $(shell command -v root-config 2>/dev/null) \
    root-config)
endif
