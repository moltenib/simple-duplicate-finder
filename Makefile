# Check the operating system
OS := $(shell uname)

all:
	@echo "Please choose 'make translations' or 'make windows'."

translations:
	@for i in resources/locales/*/LC_MESSAGES; do \
		echo "Compiling '$$i/messages.po' to '$$i/messages.mo'"; \
		msgfmt $$i/messages.po -o $$i/messages.mo; \
	done

windows:
ifeq ($(findstring MINGW,$(OS)),)
	@echo 'Skipping Windows compilation.'
else
	windres resources/version.rc -o resources/version.res
	time pyinstaller --onefile --name simple-duplicate-finder \
		--add-data "resources/icons;resources/icons" \
		--add-data "resources/locales;resources/locales" \
		--add-data "resources/version.res;resources/version.res" \
		--icon=resources/icons/app_icon.ico \
		src/main.pyw
endif

