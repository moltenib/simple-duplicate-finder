gettext:
	@for i in resources/locales/*/LC_MESSAGES; do \
		echo "Compiling '$$i/messages.po' to '.../messages.mo'"; \
		msgfmt $$i/messages.po -o $$i/messages.mo; \
	done

