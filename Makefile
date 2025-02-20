# Check the operating system
OS := $(shell uname)

all:
	@echo "Please choose 'make translations' or 'make windows'."

translations: resources/locales/*/LC_MESSAGES/messages.po
	@for i in resources/locales/*/LC_MESSAGES; do \
		echo "Compiling '$$i/messages.po' to '$$i/messages.mo'"; \
		msgfmt $$i/messages.po -o $$i/messages.mo; \
	done

windows:
ifeq ($(findstring MINGW,$(OS)),)
	@echo 'Windows not detected; skipping Windows compilation.'
else
	time pyinstaller --onefile --name simple-duplicate-finder \
		--add-data "resources/icons;resources/icons" \
		--add-data "resources/locales;resources/locales" \
		--distpath=../repo/dist \
		--icon=resources/icons/app_icon.ico \
		--version-file=resources/version.txt \
		src/main.pyw
endif

