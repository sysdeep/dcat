


run-example:
	go run ./cmd/dcat_gio --volume /tmp/example-db

run-fyne:
	go run ./cmd/dcat_fyne --volume /tmp/example-db

run-fyne-bss:
	go run ./cmd/dcat_fyne_bss --volume /tmp/example-db

example-db:
	go run ./cmd/scanner/ --scan-path /tmp/ --target-path /tmp/example-db --name "Foo"


# pro -------------------------------------------------------------------------

run-pro:
	go run ./cmd/dcat_pro --storage ../../../example_pro/

test-bssv2:
	go test -v ./internal/bssv2/

run-pro-create:
	go run ./cmd/dcat_pro_cli/ --scan-path /tmp/ --target-path /tmp/pro.gz -name pro


run-pro-sqlite:
	go run ./cmd/dcat_pro_sqlite/ --scan-path /tmp/ --target-path /tmp/pro.sqlite -name pro



# utils -----------------------------------------------------------------------
make icons:
	go run ./cmd/gio_icons/