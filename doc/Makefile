O := output

BUILD_CONFIG_FILE := CCL_Tools_User_Manual.conf
sphinx_doc_name := ccl_tools_user_manual

.PHONY: doc install-doc-src

all: doc

doc:
	mkdir -p $(O)/doc/$(sphinx_doc_name)/doc-sources
	$(realpath $(KALRAY_TOOLCHAIN_DIR)/share/doctools/tools/build_local_doc) -p $(O)/doc/$(sphinx_doc_name)/doc-sources -c $(BUILD_CONFIG_FILE) -o $(O)/doc/$(sphinx_doc_name)

clean:
	rm -rf $(O)

install-doc-src:
	mkdir -p $(PREFIX)/kalray_internal/share/doc/doc_src/$(sphinx_doc_name)
	cp -r $(O)/doc/$(sphinx_doc_name)/doc-sources/* $(PREFIX)/kalray_internal/share/doc/doc_src/$(sphinx_doc_name)/
